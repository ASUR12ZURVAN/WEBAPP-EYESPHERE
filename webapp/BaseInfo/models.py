from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=300)
    age = models.IntegerField()
    ph_Number = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class TestResult(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='test_results')
    test_type = models.CharField(max_length=100)  # e.g., 'myopia' or 'glaucoma'
    result_value = models.FloatField()            # store the numeric result (e.g., diopter)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.test_type} - {self.result_value}"