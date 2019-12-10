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
    price = float(body['price'])
    desc = body['description']
    vipfree = int(body['vipfree']) == 1
    newfood = restaurant.Food(name=name, description=desc, price=price, vip_free=vipfree, cook=my_cook)
    newfood.save()

def supply_rate(my_cook, body):
    rating = int(body['rating'])
    supplyid = int(body['supplyID'])
    supplyorder = restaurant.SupplyOrder.objects.get(id=supplyid)
    supplyorder.supply_rating = rating
    supplyorder.save()

def supply_request(my_cook, body):
    supplydes = body['supplydes']
    supplyreq = restaurant.SupplyOrder(order_description=supplydes, cook=my_cook)
    supplyreq.save()

def finishorder(my_cook, body):
    print("finishing order", int(body['orderId']))
    orderid = int(body['orderId']) # hidden input field
    order = restaurant.Order.objects.get(id=orderid)
    print(order)
    order_foods = restaurant.Order_Food.objects.filter(order=order)
    for orderfood in order_foods:
        if orderfood.food.cook == my_cook:
            orderfood.isFinished = True
            orderfood.save()
    fin_order_foods = restaurant.Order_Food.objects.filter(order=order).filter(isFinished=True)
    if len(fin_order_foods) == len(order_foods):
        order.status = 'PR'
        order.save()
        print("order", orderid, " status: ", order.status)

# Create your views here.

def home(request):
    my_user = None
    # makes sure user is deliverer
    print('cook home')
    try:
        my_user = request.user
        userIs = userTypeChecker(my_user)
        if userIs(user.Cook) != True:
            print('user not cook')
            response = redirect('home-nexus')
            return response
    except Exception as e:
        print(e)
        response = redirect('home-nexus')
        return response
    except:
        print('exception occured')
        response = redirect('home-nexus')
        return response
  
    my_cook = user.Cook.objects.get(user=my_user)
    
    registered = len(user.Cook.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_cook.status == 'H'

    if registered != True: # if not registered
        print('cook not registered')
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
        elif task=='finishorder':
            finishorder(my_cook, body)

    cookfood = restaurant.Food.objects.filter(cook=my_cook)
    supplyorders = restaurant.SupplyOrder.objects.filter(cook=my_cook)
    warnings = my_cook.warnings
    orders = restaurant.Order.objects.filter(restaurant=my_cook.restaurant)
    order_data = []
    for order in orders:
        data_entry = {
            'order': order,
            'description': order.food_description,
            'finished': len(restaurant.Order_Food.objects.filter(order=order).filter(food__cook=my_cook).filter(isFinished=True)) > 0
        }
        order_data.append(data_entry)
    # print(supplyorders)
    context = {
        'cookfood': cookfood,
        'supplyorders': supplyorders,
        'warnings': warnings,
        'orderData': order_data,
    }

    return render(request, 'cook/home.html', context=context)

def register(request):
    print('cook register')
    my_user = None
    try:
        my_user = request.user
        isType = userTypeChecker(my_user)
        if isType(user.Cook) != True:
            print('user not cook')
            response = redirect('home-nexus')
            return response
    except:
        print('user not cook')
        response = redirect('home-nexus')
        return response

    my_cook = user.Cook.objects.get(user=my_user)
    print('cook status:', my_cook.status)
    registered = len(user.Cook.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_cook.status == 'H'
    if registered:
        print('cook registered')
        return redirect('cook-home')
    registering = my_cook.restaurant == None and my_cook.status != 'H'
    print('registering:',registering)

    restaurants = restaurant.Restaurant.objects.all()
    context={'restaurants': restaurants, 'registering': registering}

    if request.method == "POST":
        body = parse_req_body(request.body)
        resturant_id = int(body['id'])
        reg_resturant = restaurant.Restaurant.objects.get(id=resturant_id)
        my_cook.restaurant = reg_resturant
        my_cook.save()
        context['registering'] = False
    return render(request, 'cook/register.html', context=context)