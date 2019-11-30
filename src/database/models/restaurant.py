from django.db import models
from database.models.user import Customer, Manager, Cook, Salesperson, Deliverer
from database.models.address import CustomerAddress

# Non user type datamodels get dumped here

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=1024)
    manager = models.OneToOneField(Manager, on_delete=models.SET_NULL, null=True)

class Order(models.Model):
    STATUS_CHOICES = [
        ('PE', 'Pending'),
        ('PR', 'Prepared'),
        ('D', 'Delivered')
    ]
    
    status = models.CharField(
        max_length = 2,
        choices = STATUS_CHOICES,
        default = "PE"
    )
    
    delivery_address = models.ForeignKey('CustomerAddress', on_delete=models.SET_NULL, null=True)
    delivery_rating = models.IntegerField(default=0)
    customer_rating = models.IntegerField(default=0) 
    total_price = models.FloatField(default=0)

class Order_Food(models.Model):
    quantity = models.IntegerField(default=0)
    isFinished = models.BooleanField(default = False)
    food_rating = models.IntegerField(default=0)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

class Food(models.Model):
    price = models.FloatField(default=0)
    name = models.CharField(max_length=50)
    description = models.TextField(blank = True)
    vip_free = models.BooleanField(default = False)
    avg_rating = models.FloatField(default=0)
    cook = models.OneToOneField(Cook, on_delete=models.CASCADE)

class SupplyOrder(models.Model):
    order_description = models.TextField()
    price = models.FloatField()
    supply_rating = models.FloatField(default = 0)
    salesperson = models.ForeignKey('Salesperson', on_delete=models.SET_NULL, null = True)
    cook = models.ForeignKey('Cook', on_delete=models.SET_NULL, null = True)

class DeliveryBid(models.Model):
    deliverer = models.ForeignKey('Deliverer', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    price = models.FloatField()
    win = models.BooleanField(default = False)

# Customer Status in Restaurant

class CustomerStatus(models.Model):
    STATUS_CHOICES = [ 
        ('B', 'Blacklisted'),
        ('N', 'Not Registered'),
        ('R', 'Registered'),
        ('V', 'VIP'),
    ]
    status = models.CharField(
        max_length = 2,
        choices = STATUS_CHOICES,
        default = "N"
    )
    order_count = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)

    def update_status(self, new_rating):
        self.avg_rating = self.order_count * self.avg_rating + new_rating / (self.order_count+1)
        self.order_count+=1

        if (self.order_count > 3):
            if (self.avg_rating == 1):
                self.status = 'B'
            elif (1 < self.avg_rating and self.avg_rating < 2):
                self.status == 'N'
            elif (self.avg_rating > 4):
                self.status == 'V'

