from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='salesperson-home'),
    path('register', views.register, name='salesperson-register'),
]