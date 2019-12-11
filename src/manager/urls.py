from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='manager-home'),
    path('deliverybids', views.deliverybids, name='manager-deliverybids'),
    path('pendingregistrations', views.pendingregistrations, name='manager-pendingregistrations'),
    path('restaurant', views.restaurant, name='manager-restaurant'),
    path('staff', views.staff, name='manager-staff'),
    re_path(r'^staffdetails/(?P<pk>\d+)$', views.staffdetails, name='manager-staffdetails'),
    path('customers', views.customers, name='manager-customers'),
    path('customerdetails/<int:pk>', views.customerdetails, name='manager-customerdetails'),
]
