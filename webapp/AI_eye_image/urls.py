from django.urls import path
from .views import AnalyzeEyeImages, eye_upload_form

urlpatterns = [
    path('', eye_upload_form, name='eye_upload_form'),
    path('analyze/', AnalyzeEyeImages.as_view(), name='analyze_eyes'),
]