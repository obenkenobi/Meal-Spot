from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models.user import Customer, Manager, Cook, Salesperson, Deliverer
from database.models.restaurant import Restaurant
from database.models.address import CustomerAddress, RestaurantAddress

# Create your views here.

def nexus(request):
    """
        This view will simply redirect the user to another
        url based on what usertype they are
    """
    return render(request, 'home/index.html', context={}) # rendering index.html for testing

def signup(request):
    """
    signup
    """
    if(request.method == "POST"):
        print("testing signup")
        print(request.body)
        body = request.body
        new_user = User.objects.create_user(body['username'], body['email'], body['password'])
        new_user.save()
        print(new_user.id)
        user_id = new_user.id
        if(body['usertype']=='customer'):
            new_customer = Customer(user=user_id)
            new_customer.save()
            new_customer_address = CustomerAddress(
                street_address = body['street-address'],
                apt = body['apt'],
                city = body['city'],
                state = body['state'],
                zip_code = body['zip-code'],
                customer = new_customer.user
            )
            new_customer_address.save()
        elif(body['usertype']=='manager'):
            new_manager = Manager(user=user_id)
            new_manager.save()
            new_resturant = Restaurant(name=body['restaurant-name'], manager=new_manager.user)
            new_resturant_address = RestaurantAddress(
                street_address = body['street-address'],
                apt = body['apt'],
                city = body
                ['city'],
                state = body['state'],
                zip_code = body['zip-code'],
                restaurant = new_resturant.id
            )
            new_resturant_address.save()
        elif(body['usertype']=='cook'):
            new_staff = Cook(user=user_id)
            new_staff.save()
        elif(body['usertype']=='salesperson'):
            new_staff = Salesperson(user=user_id)
            new_staff.save()
        elif(body['usertype']=='deliverer'):
            new_staff = Deliverer(user=user_id)
            new_staff.save()
        response = redirect('home-nexus')
        return response
    else:
        return render(request, 'home/signup.html')

