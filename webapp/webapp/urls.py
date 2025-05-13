from django.contrib import admin
from django.urls import path, include
from Myopia_Test import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', views.predict_diopters, name='predict_diopters'),
    path('', include("BaseInfo.urls")),
]
