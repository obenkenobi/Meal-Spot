from django.db import models
from database.models.user import Customer, Manager, Cook, Salesperson, Deliverer
from database.models.address import Address, CustomerAddress
from django.core.validators import RegexValidator
from functools import cmp_to_key

# Non user type datamodels get dumped here

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    manager = models.OneToOneField(Manager, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$')],
        null=True,
    )
    description = models.TextField(null=True)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    STATUS_CHOICES = [
        ('PE', 'Pending'),
        ('PR', 'Prepared'),
        ('D', 'Delivered')
    ]
    
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="PE"
    )    
    restaurant = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    delivery_rating = models.IntegerField(null=True)
    delivery_complaint = models.TextField(null=True)
    customer_rating = models.IntegerField(null=True)
    customer_complaint = models.TextField(null=True) 
    total_price = models.FloatField(default=0)
    chose_bid = models.BooleanField(default=False)

    @property
    def orderfoods(self):
        return Order_Food.objects.filter(order=self)
    
    @property
    def food_description(self):
        food_orders = self.orderfoods
        desc = ''
        for food_order in food_orders:
            desc += str(food_order.food.name) + ' x ' + str(food_order.quantity) + ','
        desc = desc[:len(desc) -1]
        return desc


# when customer adds food to order, create. if remove, delete
class Order_Food(models.Model):
    quantity = models.IntegerField(default=1)
    isFinished = models.BooleanField(default = False)
    food_rating = models.IntegerField(null=True)
    food_complaint = models.TextField(null=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    food = models.ForeignKey('Food', on_delete=models.SET_NULL, null=True)
    
    @classmethod
    def recomended(customer, restaurant):
        def cmp_food(item1, item2):
            if item1['qty'] < item2['qty']:
                return -1
            elif item1['qty'] > item2['qty']:
                return 1
            else:
                return 0
        my_orders = Order.objects.filter(customer=customer).filter(restaurant=restaurant)
        my_order_foods = Order_Food.objects.filter(order__in=my_orders)
        order_freq = {}
        for my_order_food in my_order_foods:
            food_id = my_order_food.food.id
            if order_freq.get(food_id, 0) == 0:
                order_freq[food_id] = my_order_food.quantity
            else:
                 order_freq[food_id] += my_order_food.quantity
        food_freq_list = []
        for food_id in order_freq:
            curr_food = Food.objects.get(id=food_id)
            food_freq_list.append({'food': curr_food, 'qty': order_freq[food_id]})
        food_freq_list = sorted(food_freq_list, key=cmp_to_key(cmp_food))
        if len(food_freq_list) > 3:
            food_freq_list = food_freq_list[len(food_freq_list)-3: len(food_freq_list)]
        rec_foods = [item['food'] for item in food_freq_list]
        return rec_foods
   
    @classmethod
    def popular(customer, restaurant):
        def cmp_food(item1, item2):
            if item1['qty'] < item2['qty']:
                return -1
            elif item1['qty'] > item2['qty']:
                return 1
            else:
                return 0
        my_orders = Order.objects.filter(restaurant=restaurant)
        order_foods = Order_Food.objects.filter(order__in=my_orders)
        order_freq = {}
        for order_food in order_foods:
            food_id = order_food.food.id
            if order_freq.get(food_id, 0) == 0:
                order_freq[food_id] = order_food.quantity
            else:
                 order_freq[food_id] += order_food.quantity
        food_freq_list = []
        for food_id in order_freq:
            curr_food = Food.objects.get(id=food_id)
            food_freq_list.append({'food': curr_food, 'qty': order_freq[food_id]})
        food_freq_list = sorted(food_freq_list, key=cmp_to_key(cmp_food))
        if len(food_freq_list) > 3:
            food_freq_list = food_freq_list[len(food_freq_list)-3: len(food_freq_list)]
        pop_foods = [item['food'] for item in food_freq_list]
        return pop_foods

        

class Food(models.Model):
    price = models.FloatField(default=0)
    name = models.CharField(max_length=50)
    description = models.TextField(blank = True)
    vip_free = models.BooleanField(default = False)
    avg_rating = models.FloatField(default=0)
    num_ratings = models.IntegerField(default=0)
    cook = models.ForeignKey(Cook, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name)

class SupplyOrder(models.Model):
    order_description = models.TextField()
    price = models.FloatField(null=True)
    supply_rating = models.FloatField(null=True)
    supply_complaint = models.TextField(null=True)
    salesperson = models.ForeignKey('Salesperson', on_delete=models.SET_NULL, null = True)
    cook = models.ForeignKey('Cook', on_delete=models.SET_NULL, null = True)
    finished = models.BooleanField(default=False)

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
        ('P', 'Pending')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="N"
    )
    order_count = models.IntegerField(default=0)
    avg_rating = models.FloatField(null=True)
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

    def request_registration(self):
        if self.status == 'N':
            self.status = 'P'

    def approve_registration(self):
        if self.status == 'P':
            self.status = 'R'

