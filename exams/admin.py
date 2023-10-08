from django.contrib import admin
from .models import TypesExams, MedicalTestInquiries, ExaminationOrders

admin.site.register(TypesExams)
admin.site.register(MedicalTestInquiries)
admin.site.register(ExaminationOrders)
