from django.contrib import admin

# Importing all models
from database.models.users import Customer, Manager, Cook, SalesPerson, DeliveryPerson # importing all user types

# Register your models here.

admin.site.register(Customer)
admin.site.register(Manager)
admin.site.register(Cook)
admin.site.register(SalesPerson)
admin.site.register(DeliveryPerson)
