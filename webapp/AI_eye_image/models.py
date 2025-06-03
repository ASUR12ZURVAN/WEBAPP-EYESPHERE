from django.db import models

# Create your models here.
class User_image(models.Model):
    left_eye = models.ImageField()
    right_eye = models.ImageField()

    responses = models.CharField(max_length=50000)

    
