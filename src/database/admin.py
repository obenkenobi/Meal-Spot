from django.contrib import admin

# Importing all models
from database.models.user import Customer, Manager, Cook, SalesPerson, DeliveryPerson # importing all user types
from database.models.resturant import Resturant

# Register your models here.

admin.site.register(Customer)
admin.site.register(Manager)
admin.site.register(Cook)
admin.site.register(SalesPerson)
admin.site.register(DeliveryPerson)
admin.site.register(Resturant)
