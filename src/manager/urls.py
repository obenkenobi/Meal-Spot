from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='manager-home'),
    path('deliverybids', views.deliverybids, name='manager-deliverybids'),
    path('pendingregistrations', views.pendingregistrations, name='manager-pendingregistrations'),
    path('restaurant', views.restaurant, name='manager-restaurant'),
    path('staff', views.staff, name='manager-staff'),
    path('staff-details/<int:pk>', views.staff_details, name='manager-staff_details'),
    path('customers', views.customers, name='manager-customers'),
    path('customer-details/<int:pk>', views.customer_details, name='manager-customer_details'),
]
