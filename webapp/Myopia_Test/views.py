import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import MyopiaAppResult

@csrf_exempt
def submit_app_result(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        user = User.objects.get(pk=user_id)
        data = json.loads(request.body.decode('utf-8'))

        left_eye = data.get("left_eye_diopter")
        right_eye = data.get("right_eye_diopter")

        if not left_eye or not right_eye:
            return JsonResponse({'error': 'Both eye results required'}, status=400)

        result = MyopiaAppResult.objects.create(
            user=user,
            left_eye_diopter=left_eye,
            right_eye_diopter=right_eye
        )

        return JsonResponse({
            'message': 'App result saved successfully',
            'id': result.id
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def app_results_page(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    results = request.user.myopia_app_results.all().order_by('-date_taken')
    return render(request, "app_results.html", {"results": results})


