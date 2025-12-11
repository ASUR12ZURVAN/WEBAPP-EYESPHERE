from django.db import models
from django.utils.timezone import localtime
from BaseInfo.models import User


class AISummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_summaries')
    summary_text = models.TextField()
    raw_ai_response = models.JSONField(null=True, blank=True)  # AI full response
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        date_str = localtime(self.date_created).strftime("%b %d, %Y %I:%M %p")
        return f"AI Summary for {self.user.name} ({date_str})"
