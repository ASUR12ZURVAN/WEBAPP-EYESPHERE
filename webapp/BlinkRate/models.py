from django.db import models

# Create your models here.
# models.py
from django.db import models

class BlinkRate(models.Model):
    rate = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
