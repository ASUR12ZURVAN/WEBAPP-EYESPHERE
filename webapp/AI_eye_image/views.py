from django.shortcuts import render
import os
# Create your views here.
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import User_image
from BaseInfo.models import User
from .serializers import UserImageSerializer
from decouple import config
import base64

api_key = config("OPENAI_API_KEY")
# Ensure you have set your OpenAI API key in your environment variables

def eye_upload_form(request):
    return render(request, 'analyze.html')

def call_llm_with_prompt(left_image, right_image):
    url = "https://api.openai.com/v1/chat/completions"
    model = "gpt-4o"

    # Base64 encode both images
    left_b64 = base64.b64encode(left_image.read()).decode('utf-8')
    right_b64 = base64.b64encode(right_image.read()).decode('utf-8')

    prompt = "Analyze these eye images for any signs of defects or diseases. Be specific and provide possible conditions if any."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{left_image.content_type};base64,{left_b64}"}},
                    {"type": "image_url", "image_url": {"url": f"data:{right_image.content_type};base64,{right_b64}"}}
                ]
            }
        ],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"OpenAI API Error: {response.status_code} - {response.text}")

    return response.json()["choices"][0]["message"]["content"]



class AnalyzeEyeImages(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = UserImageSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            left_eye = request.FILES.get('left_eye')
            right_eye = request.FILES.get('right_eye')
            if not left_eye or not right_eye:
                return Response({'error': 'Both eye images are required.'}, status=400)

            try:
                llm_response = call_llm_with_prompt(left_eye, right_eye)
            except Exception as e:
                return Response({'error': f'LLM API call failed: {str(e)}'}, status=500)

            user_image = User_image.objects.create(
                user=user,
                left_eye=left_eye,
                right_eye=right_eye,
                responses=llm_response
            )

            return Response({'message': 'Analysis complete', 'response': llm_response}, status=201)
        else:
            print("Serializer errors:", serializer.errors)  # Add this
            return Response(serializer.errors, status=400) 

    
    


def get_user_images(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': 'You must be logged in to view your images.'})

    user_images = User_image.objects.filter(user=user)
    return render(request, 'user_images.html', {'user_images': user_images})

