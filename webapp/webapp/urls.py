from django.contrib import admin
from django.urls import path, include
from Myopia_Test.views import predict_diopters

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', predict_diopters, name='predict_diopters'),
    path('', include("BaseInfo.urls")),
]
