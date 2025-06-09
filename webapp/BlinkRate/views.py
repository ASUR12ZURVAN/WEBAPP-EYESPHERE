from django.shortcuts import render

# Create your views here.
# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now
from .models import BlinkRate
import json

@csrf_exempt
def save_blink_rate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rate = data.get('rate')
        BlinkRate.objects.create(rate=rate, timestamp=now())
        return JsonResponse({'status': 'success', 'rate': rate})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def Blink_Rate(request):
    return render(request,"blink.html")
