from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='deliverer-home'),
    path('register', views.register, name='deliverer-register'),
    path('order/<int:pk>', views.order, name='deliverer-order'),
]