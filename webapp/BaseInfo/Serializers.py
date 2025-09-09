from rest_framework import serializers
from .models import User,TestResult,ColorVisionPlateResponse,ColorVisionTest,MyopiaAppResult

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'ph_Number', 'city', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

class ColorVisionTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVisionTest
        fields = '__all__'

class ColorVisionPlateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVisionPlateResponse
        fields = '__all__'
class MyopiaAppResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyopiaAppResult
        fields = ["id", "left_eye_diopter", "right_eye_diopter", "date_taken"]
        read_only_fields = ["id", "date_taken"]