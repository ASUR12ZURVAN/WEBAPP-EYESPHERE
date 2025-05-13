from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,TestResult
from .Serializers import UserSerializer,ResultSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from collections import defaultdict
import json 

def index(request, user_id):
    request.session['user_id'] = user_id  # store in session
    user = get_object_or_404(User, id=user_id)
    return render(request, 'hd.html', {'user': user})
def next(request):
    return render(request,'Game.html' )

@api_view(['GET', 'POST'])
def create_user(request):
    if request.method == 'POST':
        data = request.data if request.content_type == 'application/json' else request.POST
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.instance.id
            request.session['user_id'] = user_id  # ✅ store in session
            return redirect('base_myopia', user_id=user_id)
            if request.content_type == 'application/json':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # redirect to Myopia_Test/ after successful HTML form submission
        if request.content_type == 'application/json':
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'create_user.html', {'errors': serializer.errors})

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
    test_results = user.test_results.all().order_by('-date_taken')
    return render(request, 'user_profile.html', {
        'user': user,
        'test_results': test_results
    })

@csrf_exempt
def submit_score(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid request'}, status=405)

    try:
        data = json.loads(request.body)
        test_type = data.get('test_type')
        final_score = data.get('final_score')
        result_value = 0
        if test_type == "myopia":
            result_value = final_score

        # Get user_id from session
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User ID not found in session'}, status=400)

        # Fetch the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)

        # Save test result
        TestResult.objects.create(user=user, test_type=test_type, final_score=final_score)

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

    users = User.objects.all()
    test_results = TestResult.objects.all()

    # Filter test results by user_id if user_id is found in session
    test_results = test_results.filter(user_id=user_id)

    if selected_test_type:
        test_results = test_results.filter(test_type=selected_test_type)

    grouped_results = defaultdict(list)
    for result in test_results.select_related('user'):
        grouped_results[result.user].append(result)

    context = {
        'users': users,
        'grouped_results': dict(grouped_results),
        'selected_user_id': user_id,
        'selected_test_type': selected_test_type,
    }

    return render(request, 'test_results_history.html', context)
