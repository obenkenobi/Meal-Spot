from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="customer-home"),
    path("orders", views.orders, name="customer-orders"),
    path("restaurant/<int:pk>", views.resturant_page, name="customer-restaurant"),
    path("restaurant/order/<int:pk>", views.resturant_order, name="customer-restaurant-order"),
]