from django.db import models
from django.utils.timezone import localtime

class User(models.Model):
    name = models.CharField(max_length=300)
    age = models.IntegerField()
    ph_Number = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.city})"

class TestResult(models.Model):
    TEST_CHOICES = (
        ('myopia', 'Myopia'),
        ('glaucoma', 'Glaucoma'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    test_type = models.CharField(max_length=100, choices=TEST_CHOICES)
    final_score = models.DecimalField(max_digits=5,decimal_places=2)
    result_value = models.FloatField(null = True)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        unit = "diopters" if self.test_type == "myopia" else "mmHg" if self.test_type == "glaucoma" else ""
        date_str = localtime(self.date_taken).strftime("%b %d, %Y %I:%M %p")
        return f"{self.user.name} - {self.test_type.title()} - {self.result_value} {unit} ({date_str})"
