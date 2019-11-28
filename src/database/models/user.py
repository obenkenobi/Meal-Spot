from django.db import models
from django.contrib.auth.models import User # This is so the built in user is added

# Write down user models here

# Abstract UserType model/class
class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta: # Makes sure it is an abstract user model/class
        abstract = True

# Abstract Staff Class

class Staff(UserType):
    STATUS_CHOICES = [ # No need for status table, this also works
        ('L', 'Laif Off'),
        ('N', 'Not Hired'),
        ('H', 'Hired')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="N"
    )
    warnings = models.IntegerField(default=0)
    resturant = models.ForeignKey('Resturant', on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


# Non-Staff user types

class Customer(UserType):
    order_count = models.IntegerField(default=0)
    pass


class Manager(UserType):
    pass # All needed fields are inhereted, resturant references manager


# Staff User Types

class Cook(Staff):
    food_drop_count = models.IntegerField(default=0)

class DeliveryPerson(Staff):
    pass # All needed fields are inhereted

class SalesPerson(Staff):
    # TODO: Add the following
    # Commission (I don't know the purpose of that in the ER diagram????? ~ Oren)
    pass