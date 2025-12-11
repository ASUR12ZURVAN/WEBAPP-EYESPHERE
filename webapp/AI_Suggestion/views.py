import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from BaseInfo.models import (
    User, TestResult, MyopiaResult, DryEyeResult,
    GlaucomaResult, ColorVisionTest, MyopiaAppResult
)
from .models import AISummary


class AISuggestionView(APIView):

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # ---------------- Collect All Test Data ----------------
        myopia = list(MyopiaResult.objects.filter(user=user).values())
        myopia_app = list(MyopiaAppResult.objects.filter(user=user).values())
        dry_eye = list(DryEyeResult.objects.filter(user=user).values())
        glaucoma = list(GlaucomaResult.objects.filter(user=user).values())
        color_vision = list(ColorVisionTest.objects.filter(user=user).values())
        general_tests = list(TestResult.objects.filter(user=user).values())

        full_report = {
            "user": {"name": user.name, "age": user.age, "city": user.city},
            "myopia_tests": myopia,
            "myopia_app_tests": myopia_app,
            "dry_eye_tests": dry_eye,
            "glaucoma_tests": glaucoma,
            "color_vision_tests": color_vision,
            "general_tests": general_tests,
        }

        # ---------------- Groq API Call ----------------
        api_key = settings.GROQ_API_KEY

        url = "https://api.groq.com/openai/v1/chat/completions"

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a medical professional specializing in ophthalmology. "
                        "Given the user's complete eye test results, produce an accurate, "
                        "professional medical summary. Provide:\n"
                        "1. Summary of findings\n"
                        "2. Possible medical interpretation\n"
                        "3. Risk factors\n"
                        "4. Suggested next steps for the patient\n"
                        "5. Whether they should visit a specialist\n"
                        "Use simple and understandable language."
                    )
                },
                {
                    "role": "user",
                    "content": f"Here are the complete test results: {full_report}"
                }
            ],
            "temperature": 0.3,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return Response(
                {"error": "Failed to fetch AI response", "details": response.json()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        ai_text = response.json()['choices'][0]['message']['content']

        # ---------------- SAVE TO DATABASE ----------------
        saved = AISummary.objects.create(
            user=user,
            summary_text=ai_text,
            raw_ai_response=response.json()
        )

        return Response(
            {
                "message": "AI summary generated successfully",
                "summary_id": saved.id,
                "ai_summary": saved.summary_text,
                "raw_response": saved.raw_ai_response,
            },
            status=status.HTTP_200_OK
        )
