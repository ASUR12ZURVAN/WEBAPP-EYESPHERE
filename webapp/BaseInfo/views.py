from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,TestResult,ColorVisionPlateResponse,ColorVisionTest,DryEyeResult
from .Serializers import UserSerializer,ResultSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from collections import defaultdict
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from BlinkRate.models import BlinkRate
import json 

def home(request):
    return render(request,"home.html")
def index(request ):
    return render(request, 'hd.html', )

def osdi(request):
    return render(request,"osdi.html")

def mainx(request,user_id):
    request.session['user_id'] = user_id  # store in session
    user = get_object_or_404(User, id=user_id)
    return render(request, 'f.html', {'user': user})

def next(request):
    return render(request,'Game.html' )


@api_view(['GET', 'POST'])
def create_user(request):
    if request.method == 'POST':
        data = request.data if request.content_type == 'application/json' else request.POST

        # Check if user already exists
        if User.objects.filter(ph_Number=data.get('ph_Number')).exists():
            error = {'error': 'User with this phone number already exists'}
            if request.content_type == 'application/json':
                return Response(error, status=500)
            return render(request, 'create_user.html', {'errors': error})

        # Hash the password before saving
        mutable_data = data.copy()
        mutable_data['password'] = make_password(data.get('password'))

        serializer = UserSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.instance.id
            request.session['user_id'] = user_id

            if request.content_type == 'application/json':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return redirect('sign_in_user')

        # Invalid data
        if request.content_type == 'application/json':
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'create_user.html', {'errors': serializer.errors})

    # GET request: render the form
    return render(request, 'create_user.html')

def save_test_result(request, user_id, test_type, prediction_value):
    user = User.objects.get(id=user_id)
    TestResult.objects.create(
        user=user,
        test_type=test_type,
        result_value=prediction_value
    )

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Existing test results (from your TestResult model)
    test_results = user.test_results.all().order_by('-date_taken')

    # New color vision test results
    color_vision_tests = user.color_vision_tests.all().order_by('-date_taken')

    blink_rates = BlinkRate.objects.filter(user=user).order_by('-timestamp')
    dryeye_results = user.dryeye_results.all().order_by('-date_taken')

    return render(request, 'user_profile.html', {
        'user': user,
        'test_results': test_results,
        'color_vision_tests': color_vision_tests,
        'blink_rates': blink_rates,
        'dryeye_results': dryeye_results
    })


@csrf_exempt
def submit_score(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid request'}, status=405)
    
    try:
        data = json.loads(request.body)
        test_type = data.get('test_type')
        final_score = data.get('final_score')
        result_value = data.get('result_value')  # This contains "score - category"
        
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User ID not found in session'}, status=400)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
        
        if test_type == 'dryeye':
            # Extract category from result_value (format: "score - category")
            category = result_value.split(' - ')[1] if ' - ' in result_value else 'Normal'
            
            DryEyeResult.objects.create(
                user=user,
                osdi_score=final_score,
                severity=category
            )
        else:
            # Handle other test types with existing TestResult model
            TestResult.objects.create(
                user=user,
                test_type=test_type,
                final_score=final_score,
                result_value=final_score
            )
        
        return JsonResponse({'status': 'success'})
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def test_results_history(request):
    # Get user_id from session
    user_id = request.session.get('user_id')

    # If user_id is not found in session, redirect to login or error page
    if not user_id:
        return redirect('login')  # Or render an error page

    selected_test_type = request.GET.get('test_type')

    # Filter TestResult by user
    test_results = TestResult.objects.filter(user_id=user_id)
    if selected_test_type:
        test_results = test_results.filter(test_type=selected_test_type)

    # Filter ColorVisionTest by user
    color_vision_tests = ColorVisionTest.objects.filter(user_id=user_id)

    # Group TestResult by user (in this case only one user)
    grouped_test_results = defaultdict(list)
    for result in test_results.select_related('user'):
        grouped_test_results[result.user].append(result)

    # Group ColorVisionTest by user
    grouped_color_tests = defaultdict(list)
    for color_test in color_vision_tests.select_related('user'):
        grouped_color_tests[color_test.user].append(color_test)

    context = {
        'users': User.objects.all(),
        'grouped_results': dict(grouped_test_results),
        'grouped_color_tests': dict(grouped_color_tests),
        'selected_user_id': user_id,
        'selected_test_type': selected_test_type,
    }

    return render(request, 'test_results_history.html', context)

def Colour_Blindness_Test(request):
    return render(request,"Colourblindness_test.html")

class ColorVisionTestView(APIView):
    def post(self, request):
        data = request.data 

        # ✅ Get user_id from session first
        user_id = request.session.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Create ColorVisionTest instance
        test = ColorVisionTest.objects.create(
            user=user,  # <-- Fix: added comma
            normal_correct=data.get('normal_correct', 0),
            red_green_errors=data.get('red_green_errors', 0),
            protanopia_indicators=data.get('protanopia_indicators', 0),
            deuteranopia_indicators=data.get('deuteranopia_indicators', 0),
            severity_level=data.get('severity_level', 'none'),
            diagnosis_text=data.get('diagnosis_text', '')
        )

        return Response({'detail': 'Color vision test submitted successfully.'}, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'POST'])
def sign_in_user(request):
    if request.method == 'POST':
        data = request.data if request.content_type == 'application/json' else request.POST

        phone = data.get('ph_Number')
        name = data.get('name')
        raw_password = data.get('password')

        try:
            user = User.objects.get(name=name, ph_Number=phone)
        except User.DoesNotExist:
            error = {'error': 'User not found'}
            if request.content_type == 'application/json':
                return Response(error, status=status.HTTP_404_NOT_FOUND)
            return render(request, 'sign_in.html', {'errors': error})

        if check_password(raw_password, user.password):
            # Password is correct
            request.session['user_id'] = user.id  # Set session

            if request.content_type == 'application/json':
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # Redirect to user profile page with user id as parameter
            return redirect('mainx',user_id=user.id)
        else:
            error = {'error': 'Incorrect password'}
            if request.content_type == 'application/json':
                return Response(error, status=status.HTTP_401_UNAUTHORIZED)
            return render(request, 'sign_in.html', {'errors': error})

    # For GET request, just render sign-in form
    return render(request, 'sign_in.html')