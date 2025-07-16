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

class MyopiaResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myopia_results')
    left_eye_diopter = models.FloatField()
    right_eye_diopter = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        date_str = localtime(self.date_taken).strftime("%b %d, %Y %I:%M %p")
        return f"{self.user.name} - Myopia Test - L: {self.left_eye_diopter}D, R: {self.right_eye_diopter}D ({date_str})"
    
class DryEyeResult(models.Model):
    SEVERITY_CHOICES = (
        ('Normal', 'Normal'),
        ('Mild', 'Mild Dry Eye Disease'),
        ('Moderate', 'Moderate Dry Eye Disease'),
        ('Severe', 'Severe Dry Eye Disease'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dryeye_results')
    osdi_score = models.DecimalField(max_digits=5, decimal_places=2)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    date_taken = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        date_str = localtime(self.date_taken).strftime("%b %d, %Y %I:%M %p")
        return f"{self.user.name} - Dry Eye - {self.osdi_score} ({self.severity}) - ({date_str})"
    
class GlaucomaResult(models.Model):
    SEVERITY_CHOICES = (
        ('Normal', 'Normal Vision'),
        ('Mild Defect', 'Mild Peripheral Vision Defect'),
        ('Moderate Defect', 'Moderate Peripheral Vision Defect'),
        ('Severe Defect', 'Severe Peripheral Vision Defect'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='glaucoma_results')
    total_score = models.DecimalField(max_digits=5, decimal_places=2)  # Average score across 3 levels
    total_correct = models.IntegerField()  # Total correct answers out of 15
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    viewing_distance = models.IntegerField(default=60)  # Distance in cm
    date_taken = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        date_str = localtime(self.date_taken).strftime("%b %d, %Y %I:%M %p")
        return f"{self.user.name} - Glaucoma - {self.total_score}% ({self.severity}) - ({date_str})"

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


class PatientHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_history')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.name if hasattr(self.user, 'name') else self.user.username} - Patient History"

class ChiefComplaint(models.Model):
    COMPLAINT_CHOICES = [
        ('blurry_vision', 'Blurry vision'),
        ('diminution_vision', 'Diminution of vision'),
        ('pain', 'Pain'),
        ('irritation', 'Irritation'),
        ('redness', 'Redness'),
        ('injury_trauma', 'Injury / Trauma'),
        ('watering', 'Watering'),
        ('discharge', 'Discharge'),
        ('dryness', 'Dryness'),
        ('itching', 'Itching'),
        ('foreign_body', 'Foreign body sensation'),
        ('deviation_squint', 'Deviation / Squint'),
        ('headache_strain', 'Headache / Strain'),
        ('swelling', 'Swelling'),
        ('burning_sensation', 'Burning sensation'),
        ('discoloration', 'Discoloration of eye'),
        ('other', 'Other'),
    ]
    
    patient_history = models.ForeignKey(PatientHistory, on_delete=models.CASCADE, related_name='chief_complaints')
    complaint = models.CharField(max_length=50, choices=COMPLAINT_CHOICES)
    other_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_complaint_display()}"

class OphthalmicHistory(models.Model):
    OPHTHALMIC_CHOICES = [
        ('glaucoma', 'Glaucoma'),
        ('retinal_detachment', 'Retinal detachment'),
        ('glasses_use', 'Glasses use'),
        ('eye_disease', 'Eye disease'),
        ('eye_surgery', 'Eye surgery'),
        ('uveitis', 'Uveitis'),
        ('retinal_laser', 'Retinal laser treatment'),
        ('contact_lens', 'Contact lens use'),
        ('other', 'Other'),
    ]
    
    patient_history = models.ForeignKey(PatientHistory, on_delete=models.CASCADE, related_name='ophthalmic_histories')
    history_item = models.CharField(max_length=50, choices=OPHTHALMIC_CHOICES)
    other_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_history_item_display()}"

class SystemicHistory(models.Model):
    SYSTEMIC_CHOICES = [
        ('diabetes', 'Diabetes'),
        ('hypertension', 'Hypertension'),
        ('alcoholism', 'Alcoholism'),
        ('smoking_tobacco', 'Smoking tobacco'),
        ('cardiac_disorder', 'Cardiac disorder'),
        ('steroid_intake', 'Steroid intake'),
        ('drug_abuse', 'Drug abuse'),
        ('hiv_aids', 'HIV / AIDS'),
        ('tuberculosis', 'Tuberculosis'),
        ('asthma', 'Asthma'),
        ('cns_disorder', 'CNS disorder / Stroke'),
        ('hyperthyroidism', 'Hyperthyroidism'),
        ('hypothyroidism', 'Hypothyroidism'),
        ('hepatitis_cirrhosis', 'Hepatitis / Cirrhosis'),
        ('renal_disorder', 'Renal disorder'),
        ('acidity', 'Acidity'),
        ('on_insulin', 'On insulin'),
        ('blood_thinners', 'On aspirin / blood thinners'),
        ('consanguinity', 'Consanguinity'),
        ('thyroid_disorder', 'Thyroid disorder'),
        ('chewing_tobacco', 'Chewing tobacco'),
        ('chronic_kidney', 'Chronic kidney disease'),
        ('rheumatoid_arthritis', 'Rheumatoid arthritis'),
        ('other', 'Other'),
    ]
    
    patient_history = models.ForeignKey(PatientHistory, on_delete=models.CASCADE, related_name='systemic_histories')
    history_item = models.CharField(max_length=50, choices=SYSTEMIC_CHOICES)
    other_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_history_item_display()}"

class FamilyHistory(models.Model):
    FAMILY_CHOICES = [
        ('glaucoma', 'Glaucoma'),
        ('keratoconus', 'Keratoconus'),
        ('myopia', 'Myopia'),
        ('other', 'Other'),
    ]
    
    patient_history = models.ForeignKey(PatientHistory, on_delete=models.CASCADE, related_name='family_histories')
    history_item = models.CharField(max_length=50, choices=FAMILY_CHOICES)
    other_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_history_item_display()}"

class DrugAllergy(models.Model):
    DRUG_ALLERGY_CHOICES = [
        ('antimicrobial_agents', 'Antimicrobial agents'),
        ('antifungal_agents', 'Antifungal agents'),
        ('eye_drops', 'Eye drops'),
        ('other', 'Other'),
    ]
    
    patient_history = models.ForeignKey(PatientHistory, on_delete=models.CASCADE, related_name='drug_allergies')
    allergy_type = models.CharField(max_length=50, choices=DRUG_ALLERGY_CHOICES)
    other_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_allergy_type_display()}"

class ContactAllergy(models.Model):
    CONTACT_ALLERGY_CHOICES = [
        ('alcohol', 'Alcohol'),
        ('betadine', 'Betadine'),
        ('other', 'Other'),
    ]
    
    patient_history = models.ForeignKey(PatientHistory, on_delete=models.CASCADE, related_name='contact_allergies')
    allergy_type = models.CharField(max_length=50, choices=CONTACT_ALLERGY_CHOICES)
    other_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_allergy_type_display()}"