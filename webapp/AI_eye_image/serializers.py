from rest_framework import serializers
from .models import User_image
from BaseInfo.models import User

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_image
        fields = ['id', 'user', 'left_eye', 'right_eye', 'responses']
