from django.shortcuts import render

def predict_diopters(request):
    if request.method == 'POST':
        try:
            line_number = int(request.POST.get('lineNumber'))
            logmar = (10 - line_number) * 0.1
            raw_diopters = 3.3 * logmar
            prediction = round(raw_diopters * 2) / 2.0

            context = {
                'prediction': prediction,
                'user': request.user,             # ← make user available
            }
        except Exception as e:
            print("Prediction error:", e)
            context = {
                'prediction': "Invalid input",
                'user': request.user,             # ← still pass user
            }
    else:
        context = {
            'prediction': "Invalid request method",
            'user': request.user,                 # ← still pass user
        }

    return render(request, 'prediction_result.html', context)
