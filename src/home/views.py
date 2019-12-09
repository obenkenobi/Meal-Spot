from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models.user import Customer, Manager, Cook, Salesperson, Deliverer
from database.models.restaurant import Restaurant
from database.models.address import CustomerAddress, RestaurantAddress, Address
from helper import parse_req_body, userTypeChecker

# Create your views here.

def nexus(request):
    """
        This view will simply redirect the user to another
        url based on what usertype they are
    """
    user = request.user
    userIs = userTypeChecker(user)
    response = None
    try:
        if userIs(Manager):
            print('redirecting to manager-home')
            response = redirect('manager-home')
        elif userIs(Deliverer):
            print('redirecting to deliverer-home')
            response = redirect('deliverer-home')
        elif userIs(Cook):
            print('redirecting to cook-home')
            response = redirect('cook-home')
        elif userIs(Salesperson):
            print('redirecting to salesperson-home')
            response = redirect('salesperson-home')
        else:
            print('redirecting to customer-home')
            response = redirect('customer-home')
    except:
        print('redirecting to customer-home')
        response = redirect('customer-home')
    return response

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
        states = [choice[1] for choice in Address.STATE_CHOICES]
        return render(request, 'home/signup.html', {'states': states})

