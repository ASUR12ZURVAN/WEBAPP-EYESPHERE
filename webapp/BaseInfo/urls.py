from django.contrib import admin
from django.urls import path, include
from Myopia_Test.views import predict_diopters
from . import views

urlpatterns = [
    path('', views.index, name = "base_myopia"),
]
