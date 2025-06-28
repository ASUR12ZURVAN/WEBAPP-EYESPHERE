from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").lower().strip()
            
            if not message:
                return JsonResponse({"reply": "What is your eye issue?"})
            
            # Check for all symptoms and collect tests
            tests_needed = set()
            
            if any(word in message for word in ['red', 'redness', 'bloodshot', 'inflamed']):
                tests_needed.add('Vision Distance Test')
                tests_needed.add('Eye Pressure Test')
            
            if any(word in message for word in ['blurry', 'blur', 'focus', 'unclear', 'fuzzy']):
                tests_needed.add('Vision Distance Test')
                tests_needed.add('OSDI Test')
            
            if any(word in message for word in ['dry', 'dryness', 'burning', 'itchy', 'irritated']):
                tests_needed.add('Vision Distance Test')
                tests_needed.add('OSDI Test')
            
            if any(word in message for word in ['pain', 'ache', 'pressure', 'headache']):
                tests_needed.add('Vision Distance Test')
                tests_needed.add('Eye Pressure Test')
            
            if any(word in message for word in ['color', 'colour', 'colors', 'colours']):
                tests_needed.add('Colour Vision Test')
            
            if any(word in message for word in ['peripheral', 'side', 'corner', 'field']):
                tests_needed.add('Eye Pressure Test')
            
            # Generate reply based on collected tests
            if tests_needed:
                tests_list = list(tests_needed)
                if len(tests_list) == 1:
                    reply = f"You have to test {tests_list[0]}."
                elif len(tests_list) == 2:
                    reply = f"You have to test {tests_list[0]} and {tests_list[1]}."
                else:
                    reply = f"You have to test {', '.join(tests_list[:-1])} and {tests_list[-1]}."
            else:
                reply = "What is your eye issue? Please describe your symptoms."
            
            return JsonResponse({"reply": reply})
            
        except Exception as e:
            return JsonResponse({"reply": "What is your eye issue?"})
    
    return JsonResponse({"error": "POST request required"}, status=405)

def chat_page(request):
    return render(request, 'chat.html')