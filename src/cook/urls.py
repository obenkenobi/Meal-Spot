from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='cook-home'),
    path('register', views.home, name='cook-register')
]