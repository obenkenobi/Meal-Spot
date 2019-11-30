from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models.user import Customer, Manager, Cook, Salesperson, Deliverer
from database.models.restaurant import Restaurant
from database.models.address import CustomerAddress, RestaurantAddress
from helper import parse_req_body

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
        body = parse_req_body(request.body)
        print(body)
        new_user = User.objects.create_user(body['usrname'], body['email'].replace('%', '@'), body['psw'])
        new_user.save()
        print(new_user.id)
        if(body['usertype']=='cust'):
            new_customer = Customer(user=new_user)
            new_customer.save()
            new_customer_address = CustomerAddress(
                street_address = body['staddr'],
                apt = body['apt'],
                city = body['city'],
                state = body['state'],
                zip_code = body['zipcode'],
                customer = new_customer
            )
            new_customer_address.save()
        elif(body['usertype']=='mang'):
            new_manager = Manager(user=new_user)
            new_manager.save()
            new_resturant = Restaurant(name=body['restname'], manager=new_manager)
            new_resturant.save()
            new_resturant_address = RestaurantAddress(
                street_address = body['staddr'],
                apt = body['apt'],
                city = body
                ['city'],
                state = body['state'],
                zip_code = body['zipcode'],
                restaurant = new_resturant
            )
            new_resturant_address.save()
        elif(body['usertype']=='cook'):
            new_staff = Cook(user=new_user)
            new_staff.save()
        elif(body['usertype']=='salespers'):
            new_staff = Salesperson(user=new_user)
            new_staff.save()
        elif(body['usertype']=='deliverer'):
            new_staff = Deliverer(user=new_user)
            new_staff.save()
        response = redirect('home-nexus')
        return response
    else:
        return render(request, 'home/signup.html')

