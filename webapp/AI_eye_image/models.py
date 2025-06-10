from django.db import models
from BaseInfo.models import User
# Create your models here.
class User_image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Eye_Images")
    left_eye = models.ImageField()
    right_eye = models.ImageField()

    responses = models.CharField(max_length=50000)

    
