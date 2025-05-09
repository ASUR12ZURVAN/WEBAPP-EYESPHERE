from django.shortcuts import render

def predict_diopters(request):
    if request.method == 'POST':
        try:
            line_number = int(request.POST.get('lineNumber'))

            # Replace with your ML model logic if applicable
            prediction = round(-0.1 * line_number, 2)

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
