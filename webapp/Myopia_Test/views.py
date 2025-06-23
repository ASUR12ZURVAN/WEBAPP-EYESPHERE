from django.shortcuts import render
from django.urls import reverse

def predict_diopters(request):
    if request.method == 'POST':
        try:
            line_number = int(request.POST.get('lineNumber'))
            headache = request.POST.get('headache', 'no')  # Get headache value, default to 'no'
            
            logmar = (10 - line_number) * 0.1
            if line_number >= 10:
                raw_diopters = 0.0
            else:
                raw_diopters = -3.3 * logmar
            
            # Apply sign based on headache response
            if headache == 'yes':
                if raw_diopters == 0:
                    prediction = 0
                else:
                    prediction = round(abs(raw_diopters) * 2) / 2.0
            else:
                if raw_diopters == 0:
                    prediction = 0
                else:
                    prediction = -round(abs(raw_diopters) * 2) / 2.0
            
            user_id = request.session.get('user_id')
            if not user_id:
                raise Exception("User ID not found in session")
            
            context = {
                'prediction': prediction,
                'user_id': user_id,
                'headache': headache,  # Optional: pass headache status to template
            }
        
        except Exception as e:
            context = {
                'prediction': "Invalid input",
                'error': str(e),
                'user_id': request.session.get('user_id'),
            }
    
    else:
        context = {
            'prediction': "Invalid request method",
            'user_id': request.session.get('user_id'),
        }
    
    return render(request, 'prediction_result.html', context)