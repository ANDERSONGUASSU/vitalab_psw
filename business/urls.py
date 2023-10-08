from django.urls import path
from . import views

urlpatterns = [
    path('manage_clients/', views.manage_clients, name="manage_clients"),
]
