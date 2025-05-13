from django.contrib import admin
from django.urls import path, include
from Myopia_Test.views import predict_diopters
from . import views

urlpatterns = [
    path('Myopia_Test/', views.index, name = "base_myopia"),
    path('create-user/', views.create_user, name='create-user'),
    path('glaucoma_test',views.next,name = 'base_glaucoma'),
    path('submit-score/', views.submit_score, name='submit_score'),
    path('user_profile/',views.user_profile,name = 'user_profile'),
    path('results-history/', views.test_results_history, name='results_history'),
]
