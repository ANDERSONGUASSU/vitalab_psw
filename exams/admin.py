from django.contrib import admin
from .models import TypesExams, MedicalTestInquiries, ExaminationOrders, MedicalAccess # NOQA

admin.site.register(TypesExams)
admin.site.register(MedicalTestInquiries)
admin.site.register(ExaminationOrders)
admin.site.register(MedicalAccess)
