from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(TestResult)
admin.site.register(ColorVisionTest)
admin.site.register(DryEyeResult)
admin.site.register(GlaucomaResult)
admin.site.register(MyopiaResult)
admin.site.register(PatientHistory)
admin.site.register(ChiefComplaint)
admin.site.register(OphthalmicHistory)
admin.site.register(SystemicHistory)
admin.site.register(FamilyHistory)
admin.site.register(DrugAllergy)
admin.site.register(ContactAllergy)






