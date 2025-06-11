from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from BlinkRate.models import BlinkRate

@csrf_exempt
def save_blink_rate(request):
    user = request.session.get('user_id')
    if not user:
        return JsonResponse({'error': 'User not authenticated'}, status=401)    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rate = data.get('rate')

            if rate is None:
                return JsonResponse({'error': 'Rate is required'}, status=400)

            BlinkRate.objects.create(user = user,rate=rate)
            return JsonResponse({'status': 'success', 'rate': rate})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def Blink_Rate(request):
    return render(request,"blink.html")
