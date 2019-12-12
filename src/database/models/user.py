from django.db import models
from django.contrib.auth.models import User # This is so the built in user is added

# Write down user models here

# Abstract UserType model/class
class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.user)
    

    class Meta: # Makes sure it is an abstract user model/class
        abstract = True

# Abstract Staff Class

class Staff(UserType):
    STATUS_CHOICES = [ # No need for status table, this also works
        ('N', 'Not Hired'),
        ('H', 'Hired')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="N"
    )

    warnings = models.IntegerField(default=0)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    salary = models.FloatField(default = 0)
    
    def addWarning(self):
        self.warnings = self.warnings
        if self.warnings > 3:
            self.status = 'N'
            self.warnings = 0
            self.restaurant = None
        self.save()

    class Meta:
        abstract = True


# Non-Staff user types

class Customer(UserType):
    pass


class Manager(UserType):
    pass # All needed fields are inherited, restaurant references manager


# Staff User Types

class Cook(Staff):
    food_drops = models.IntegerField(default=0)

    def add_food_drops(self):
        self.food_drops = self.food_drops + 1
        if self.food_drops >= 2:
            self.food_drops = 0 
            self.addWarning()
        self.save()
    
    # prob add to Customer view during rating
    # def update_status(self, r1, r2, r3, food_id):
    # #TODO query last 2 order ratings from Orders DB based on self.restaurant, store as rating1, rating2
    #     avg_rating = (r1 + r2 + r3) / 3

    #     if avg_rating < 2:
    #         #TODO remove food from Food DB
    #         self.food_drops += 1
    #         self.warnings = self.food_drops%2

    #     if self.warnings > 3:
    #         self.status = 'N'
    #         self.restaurant = None


class Deliverer(Staff):
    avg_rating = models.FloatField(default=0)
    num_ratings = models.IntegerField(default=0)
    def add_rating(self, new_rating):
        self.avg_rating = (self.avg_rating*self.num_ratings + new_rating)/(self.num_ratings + 1)
        self.num_ratings = self.num_ratings + 1
        if self.avg_rating < 2:
            self.avg_rating = 0
            self.num_ratings = 0
            self.addWarning()
    # def update_status(self, r1, r2, r3):
    #     avg_rating = (r1 + r2 + r3) / 3

    #     if avg_rating < 2:
    #         self.warnings += 1
        
    #     if self.warnings > 3:
    #         self.status = 'N'
    #         self.restaurant = None            

class Salesperson(Staff):
    pass
    # prob add to Cook view during rating
    # def update_commission(self, r1, r2, r3):
    #     sum_rating = r1 + r2 + r3
    #     if sum_rating == 15:
    #         self.commission *= 1.1
    #     elif sum_rating <= 6:
    #         self.commission *= 0.9
    #         self.warnings += 1
        
    #     if self.warnings == 3:
    #         self.status = 'N'
    #         self.restaurant = None
