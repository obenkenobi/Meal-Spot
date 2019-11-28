from django.db import models
from django.contrib.auth.models import User # This is so the built in user is added

# Write down user models and information directly related to them here

# Abstract UserType model/class
class UserType(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta: # Makes sure it is an abstract user model/class
        abstract = True

# Abstract Staff Class

class Staff(UserType):
    # TODO: Add the following
    # Foreign Key to Resturant must be added
    # Foreign key to staff status or staff status field must be added
    # Warning count must be added (Default value is 0)

    class Meta:
        abstract = True


# Non-Staff user types

class Customer(UserType):
    # TODO: Add the following
    # Order Count (Default is Zero)
    # Foreign key to staff status or staff status field must be added
    pass


class Manager(UserType):
    # TODO: Add the following
    # Foreign Key to Resturant must be added
    # Foreign key to staff status or staff status field must be added
    pass


# Staff User Types

class Cook(Staff):
    # TODO: Add the following
    # Food drop count 
    pass

class DeliveryPerson(Staff):
    pass # All needed fields are inhereted

class SalesPerson(Staff):
    # TODO: Add the following
    # Commission
    pass