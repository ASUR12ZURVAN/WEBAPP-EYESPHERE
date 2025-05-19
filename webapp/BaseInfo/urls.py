from django.contrib import admin
from django.urls import path, include
from Myopia_Test.views import predict_diopters
from . import views
from .views import ColorVisionTestView

urlpatterns = [
    path('',views.home,name = 'home_page'),
    path('Myopia_Test/<int:user_id>/', views.index, name='base_myopia'),
    path('create-user/', views.create_user, name='create-user'),
    path('glaucoma_test/',views.next,name = 'base_glaucoma'),
    path('submit_score/', views.submit_score, name='submit_score'),
    path('user_profile/<int:user_id>/',views.user_profile,name = 'user_profile'),
    path('results_history/', views.test_results_history, name='results_history'),
    path('api/color-vision-tests/', ColorVisionTestView.as_view(), name='color-vision-test'),
    path('Colourblindness_Test/',views.Colour_Blindness_Test,name = 'Colourblindness_Test'),
    path('sign-in/', views.sign_in_user, name='sign_in_user'),
]
