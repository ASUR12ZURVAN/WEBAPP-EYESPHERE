from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from BlinkRate.models import BlinkRate
from BaseInfo.models import User
import json
from .models import BlinkRate


@csrf_exempt
@api_view(['POST'])
def save_blink_rate(request):
    try:
        user_id = request.session.get('user_id')
        print("Session user_id:", user_id)

        if not user_id:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        try:
            user = User.objects.get(id=user_id)
            print("User object:", user)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid user'}, status=401)

        data = json.loads(request.body)
        rate = data.get('rate')
        print("Rate from request:", rate)

        if rate is None:
            return JsonResponse({'error': 'Rate is required'}, status=400)

        BlinkRate.objects.create(user=user, rate=rate)
        print("Blink rate saved.")

        return JsonResponse({'status': 'success', 'rate': rate})
    except Exception as e:
        print("Exception:", str(e))
        return JsonResponse({'error': str(e)}, status=500)



def Blink_Rate(request):
    return render(request,"blink.html")
