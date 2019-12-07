from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='manager-home'),
    path('deliverybids', views.deliverybids, name='manager-deliverybids'),
    path('pendingregistrations', views.pendingregistrations, name='manager-pendingregistrations'),
    path('hirestaff', views.hirestaff, name='manager-hirestaff'),
    path('restaurant', views.restaurant, name='manager-restaurant'),
    path('staff', views.staff, name='manager-staff'),
    path('customers', views.customers, name='manager-customers'),
]
