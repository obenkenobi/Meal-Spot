from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from database.models import user, restaurant, address
from helper import parse_req_body, userTypeChecker
import django.views

# Create your views here.

def home(request):
    my_user = None
    try:
        my_user = request.user
        userIs = userTypeChecker(my_user)
        if userIs(user.Salesperson) != True:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

    my_salesperson = user.Salesperson.objects.get(user=my_user)
    registered = len(user.Salesperson.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_salesperson.status == 'H'
    if registered != True:
        return redirect('salesperson-register')

    if request.method == "POST": 
        body = parse_req_body(request.body)
        orderID= body['orderId']
        order = restaurant.SupplyOrder.objects.get(id=orderID)
        order.salesperson = my_salesperson
        order.finished = True
        order.save()
    supply_orders = restaurant.SupplyOrder.objects.filter(cook__restaurant=my_salesperson.restaurant)
    return render(request, 'salesperson/home.html', context={'warnings': my_salesperson.warnings, 'supplyOrders': supply_orders})

def register(request):
    my_user = None
    try:
        my_user = request.user
        isType = userTypeChecker(my_user)
        if isType(user.Salesperson) != True:
            response = redirect('home-nexus')
            return response
    except:
        response = redirect('home-nexus')
        return response

    my_deliverer = user.Salesperson.get(user=my_user)
    registered = len(user.Salesperson.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_deliverer.status == 'H'
    if registered:
        return redirect('salesperson-home')
    registering = len(user.Salesperson.objects.filter(user=my_user).exclude(restaurant__isnull=False)) > 0 and my_deliverer.status != 'H'

    restaurants = restaurant.Restaurant.objects.all()
    context={'restaurants': restaurants, 'registering': registering}

    if registering != True and request.method == "POST":
        body = parse_req_body(request.body)
        resturant_id = int(body['id'])
        reg_resturant = restaurant.Restaurant.objects.get(id=resturant_id)
        my_deliverer.update(restaurant = reg_resturant)
        context['registering'] = True
    return render(request, 'salesperson/register.html', context=context)

