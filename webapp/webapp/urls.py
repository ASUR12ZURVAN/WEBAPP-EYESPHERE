from django.contrib import admin
from django.urls import path, include
from Myopia_Test import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You are authenticated'})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', views.predict_diopters, name='predict_diopters'),
    path('', include("BaseInfo.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blink/',include("BlinkRate.urls")),
    path('eye/', include("AI_eye_image.urls")),
]
