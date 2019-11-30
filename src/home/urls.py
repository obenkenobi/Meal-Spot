from django.urls import path
from . import views

urlpatterns = [
    path('', views.nexus, name='home-nexus'),
    path('signup', views.signup, name='home-nexus'),
]