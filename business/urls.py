from django.urls import path
from . import views

urlpatterns = [
    path('manage_clients/', views.manage_clients, name="manage_clients"),
    path('client/<int:client_id>', views.client, name="client"),
    path('exam_client/<int:exam_id>', views.exam_client, name="exam_client"),
    path('proxy_pdf/<int:exam_id>', views.proxy_pdf, name="proxy_pdf"),
    path('generate_password/<int:exam_id>', views.generate_password,
         name="generate_password"),
    path('update_exam_data/<int:exame_id>', views.update_exam_data,
         name="update_exam_data"),

]
