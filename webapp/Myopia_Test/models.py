from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import localtime

class MyopiaAppResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myopia_app_results')
    left_eye_diopter = models.CharField(max_length=10)
    right_eye_diopter = models.CharField(max_length=10)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        date_str = localtime(self.date_taken).strftime("%b %d, %Y %I:%M %p")
        return f"{self.user.username} - App Myopia Test - L: {self.left_eye_diopter}, R: {self.right_eye_diopter} ({date_str})"
