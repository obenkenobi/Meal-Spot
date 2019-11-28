from django.db import models
from database.models.user import Customer, Manager, Cook, SalesPerson, DeliveryPerson

# Non user type datamodels get dumped here

class Resturant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=1024)
    manager = models.OneToOneField(Manager, on_delete=models.SET_NULL, null=True)