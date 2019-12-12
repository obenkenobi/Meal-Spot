from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='cook-home'),
    path('register', views.register, name='cook-register')
]