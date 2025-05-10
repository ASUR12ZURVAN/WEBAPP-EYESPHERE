from django.shortcuts import render

def predict_diopters(request):
    if request.method == 'POST':
        try:
            line_number = int(request.POST.get('lineNumber'))
            logmar = (10 - line_number)*0.1
            raw_diopters = 3.3*logmar
            # Replace with your ML model logic if applicable
            prediction = round(raw_diopters * 2)/2.0

            return render(request, 'prediction_result.html', {
                'prediction': prediction
            })

        except Exception as e:
            print("Prediction error:", e)
            return render(request, 'prediction_result.html', {
                'prediction': "Invalid input"
            })

    return render(request, 'prediction_result.html', {
        'prediction': "Invalid request method"
    })
