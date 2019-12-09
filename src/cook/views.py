from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from database.models import user, restaurant, address
from helper import parse_req_body, userTypeChecker
import django.views

# helper functions for post request
def deletefood(my_cook, body):
    food_id = int(body['foodId'])
    myfood = restaurant.Food.objects.get(id=food_id)
    myfood.delete()

def addfood(my_cook, body):
    name = body['foodname']
    desc = body['price']
    price = body['description']
    vipfree = int(body['vipfree']) == 1
    newfood = restaurant.Food(name=name, description=desc, price=price, vip_free=vipfree)
    newfood.save()

def supply_rate(my_cook, body):
    rating = int(body['rating'])
    supplyid = int(body['supplyID'])
    supplyorder = restaurant.SupplyOrder.objects.get(id=supplyid)
    supplyorder.supply_rating = rating
    supplyorder.save()

def supply_request(my_cook, body):
    supplydes = body['supplydes']
    supplyreq = restaurant.SupplyOrder(order_description=supplydes)
    supplyreq.save()

# Create your views here.

def home(request):
    my_user = None
    # makes sure user is deliverer
    try:
        my_user = request.user
        userIs = userTypeChecker(my_user)
        if userIs(user.Cook) != True:
            response = redirect('home-nexus')
            return response
    except Exception as e:
        print(e)
        response = redirect('home-nexus')
        return response
    except:
        response = redirect('home-nexus')
        return response
  
    my_cook = user.Cook.objects.get(user=my_user)
    
    registered = len(user.Cook.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_cook.status == 'H'

    if registered != True: # if not registered
        return redirect('cook-register')  
    
    if request.method == "POST":
        body = parse_req_body(request.body)
        task = body['task']
        if task == 'deletefood':
            deletefood(my_cook, body)
        elif task == 'addfood':
            addfood(my_cook, body)
        elif task=='ratesupply':
            supply_rate(my_cook, body)
        elif task=='requestsupply':
            supply_request(my_cook, body)
        pass

    cookfood = restaurant.Food.objects.filter(cook=my_cook)
    supplyorders = restaurant.SupplyOrder.objects.filter(cook=my_cook)
    warnings = my_cook.warnings

    context = {
        'cookfood': cookfood,
        'supplyorders': supplyorders,
        'warnings': warnings,
    }

    return render(request, 'cook/home.html', context=context)

def register(request):
    my_user = None
    try:
        my_user = request.user
        isType = userTypeChecker(my_user)
        if isType(user.Cook) != True:
            response = redirect('home-nexus')
            return response
    except:
        response = redirect('home-nexus')
        return response

    my_cook = user.Cook.get(user=my_user)
    registered = len(user.Cook.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_cook.status == 'H'
    if registered:
        return redirect('cook-home')
    registering = len(user.Cook.objects.filter(user=my_user).exclude(restaurant__isnull=False)) > 0 and my_cook.status != 'H'

    restaurants = restaurant.Restaurant.objects.all()
    context={'restaurants': restaurants, 'registering': registering}

    if registering != True and request.method == "POST":
        body = parse_req_body(request.body)
        resturant_id = int(body['id'])
        reg_resturant = restaurant.Restaurant.objects.get(id=resturant_id)
        my_cook.update(restaurant = reg_resturant)
        context['registering'] = True
    return render(request, 'cook/register.html', context={})