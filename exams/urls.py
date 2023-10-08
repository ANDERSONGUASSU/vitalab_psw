from django.urls import path
from . import views

urlpatterns = [
    path('medical_test_inquiries/', views.medical_test_inquiries,
         name="medical_test_inquiries"),
    path('close_order/', views.close_order,
         name="close_order"),
    path('manage_orders/', views.manage_orders, name="manage_orders"),
    path('cancel_orders/<int:order_id>', views.cancel_orders,
         name="cancel_orders"),
    path('manage_exams/', views.manage_exams, name="manage_exams"),
    path('allow_opening_exam/<int:exam_id>', views.allow_opening_exam,
         name="allow_opening_exam"),
    path('request_exam_passoword/<int:exam_id>', views.request_exam_passoword,
         name="request_exam_passoword"),
    path('generate_medical_access/', views.generate_medical_access,
         name="generate_medical_access"),
    path('medical_access/<str:token>', views.medical_access,
         name="medical_access"),

]
