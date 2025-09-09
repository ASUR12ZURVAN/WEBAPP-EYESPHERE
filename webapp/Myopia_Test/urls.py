from django.http import HttpResponse
from .views import *
from django.urls import path


urlpatterns = [
    path("submit_app_result/", submit_app_result, name="submit_app_result"),
    path("app-results/", app_results_page, name="app_results_page"),
]
