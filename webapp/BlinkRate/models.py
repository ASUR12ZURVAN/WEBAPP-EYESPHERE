from django.db import models
from BaseInfo.models import User
# Create your models here.
# models.py


class BlinkRate(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True,related_name="blink_rates")
    rate = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    
