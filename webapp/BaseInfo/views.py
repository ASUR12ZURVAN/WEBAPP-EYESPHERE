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

def index(request):
    return render(request, 'hd.html')  
def next(request):
    return render(request,'Game.html' )

@api_view(['GET', 'POST'])
def create_user(request):
    if request.method == 'POST':
        data = request.data if request.content_type == 'application/json' else request.POST
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if request.content_type == 'application/json':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # redirect to Myopia_Test/ after successful HTML form submission
            return redirect('base_myopia')
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

def submit_score(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid request'}, status=405)

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        test_type = data.get('test_type')
        final_score = data.get('final_score')
        print(user_id)

        # 1️⃣ Validate user_id presence
        if not user_id:
            return JsonResponse(
                {'status': 'error', 'message': 'Missing user_id'}, status=400
            )

        # 2️⃣ Cast to int (will catch non-numeric strings)
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid user_id'}, status=400
            )

        # 3️⃣ Lookup the user or 404
        user = get_object_or_404(User, id=user_id)

        # 4️⃣ Finally, save the result
        TestResult.objects.create(
            user=user,
            test_type=test_type,
            result_value=final_score
        )
        return JsonResponse({'status': 'success'})

    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid JSON'}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)}, status=500
        )


def test_results_history(request):
    selected_user_id = request.GET.get('user_id')
    selected_test_type = request.GET.get('test_type')

    users = User.objects.all()
    test_results = TestResult.objects.all()

    if selected_user_id:
        test_results = test_results.filter(user_id=selected_user_id)

    if selected_test_type:
        test_results = test_results.filter(test_type=selected_test_type)

    grouped_results = defaultdict(list)
    for result in test_results.select_related('user'):
        grouped_results[result.user].append(result)  # Use user object as key

    context = {
        'users': users,
        'grouped_results': dict(grouped_results),
        'selected_user_id': int(selected_user_id) if selected_user_id else '',
        'selected_test_type': selected_test_type,
    }

    return render(request, 'test_results_history.html', context)