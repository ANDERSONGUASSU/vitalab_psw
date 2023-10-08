from django.urls import path
from . import views

urlpatterns = [
    path('medical_test_inquiries/', views.medical_test_inquiries,
         name="medical_test_inquiries"),
    path('close_order/', views.close_order,
         name="close_order"),
    path('menage_orders/', views.menage_orders, name="menage_orders"),
    path('cancel_orders/<int:order_id>', views.cancel_orders,
         name="cancel_orders"),
]
