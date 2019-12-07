from django.contrib import admin

# Importing all models
from database.models.user import Customer, Manager, Cook, Salesperson, Deliverer # importing all user types
from database.models.address import CustomerAddress, RestaurantAddress
from database.models.restaurant import Restaurant, Order, Order_Food, Food, SupplyOrder, DeliveryBid, CustomerStatus

# Register your models here.

admin.site.register(Customer)
admin.site.register(Manager)
admin.site.register(Cook)
admin.site.register(Salesperson)
admin.site.register(Deliverer)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(Order_Food)
admin.site.register(Food)
admin.site.register(SupplyOrder)
admin.site.register(DeliveryBid)
admin.site.register(CustomerStatus)
admin.site.register(CustomerAddress)
admin.site.register(RestaurantAddress)
