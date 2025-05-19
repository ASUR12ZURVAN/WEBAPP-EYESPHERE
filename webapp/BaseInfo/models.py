from django.db import models
from django.utils.timezone import localtime

class User(models.Model):
    name = models.CharField(max_length=300)
    age = models.IntegerField()
    ph_Number = models.CharField(max_length=200,unique=True)
    city = models.CharField(max_length=200)
    password = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.name} ({self.city})"

class TestResult(models.Model):
    TEST_CHOICES = (
        ('myopia', 'Myopia'),
        ('glaucoma', 'Glaucoma'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    test_type = models.CharField(max_length=100, choices=TEST_CHOICES)
    final_score = models.DecimalField(max_digits=5,decimal_places=2,null=True)
    result_value = models.FloatField(null = True)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        unit = "diopters" if self.test_type == "myopia" else "mmHg" if self.test_type == "glaucoma" else ""
        date_str = localtime(self.date_taken).strftime("%b %d, %Y %I:%M %p")
        return f"{self.user.name} - {self.test_type.title()} - {self.result_value} {unit} ({date_str})"

class ColorVisionTest(models.Model):
    SEVERITY_CHOICES = (
        ('none', 'None'),
        ('weak', 'Weak'),
        ('moderate', 'Moderate'),
        ('strong', 'Strong'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='color_vision_tests')
    date_taken = models.DateTimeField(auto_now_add=True)

    normal_correct = models.PositiveIntegerField(default=0)
    red_green_errors = models.PositiveIntegerField(default=0)
    protanopia_indicators = models.PositiveIntegerField(default=0)
    deuteranopia_indicators = models.PositiveIntegerField(default=0)

    severity_level = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='none')
    diagnosis_text = models.TextField()

    def __str__(self):
        date_str = localtime(self.date_taken).strftime("%b %d, %Y %I:%M %p")
        return f"{self.user.name} - Color Vision ({self.severity_level.title()}) ({date_str})"

class ColorVisionPlateResponse(models.Model):
    test = models.ForeignKey(ColorVisionTest, on_delete=models.CASCADE, related_name='plate_responses')
    plate_number = models.PositiveIntegerField()
    user_answer = models.CharField(max_length=100)
    expected_text = models.CharField(max_length=255)
    result = models.CharField(
        max_length=10,
        choices=[
            ('correct', 'Correct'),
            ('incorrect', 'Incorrect'),
        ]
    )

    def __str__(self):
        return f"Plate {self.plate_number} - {self.result} ({self.test.user.name})"
