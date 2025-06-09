# urls.py
from django.urls import path
from .views import save_blink_rate,Blink_Rate

urlpatterns = [
    path('save_blink_rate/', save_blink_rate),
    path('Blink_Rate_Page/',Blink_Rate,name = "Blink_Page"),
]
