from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from database.models import user, restaurant, address
from helper import parse_req_body, userTypeChecker
import django.views

# Create your views here.
def home(request):
    userIs = userTypeChecker(request.user)
    if request.user.is_authenticated:
        if userIs(user.Customer) != True:
            return redirect('home-nexus')
    restaurants = restaurant.Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, "customer/home.html", context=context)

def resturant_page(request, pk):
    userIs = userTypeChecker(request.user)
    my_restaurant = restaurant.Restaurant.objects.get(id=pk)
    my_customer = None
    customer_status_info = None
    status = 'N'
    my_restaurant = restaurant.Restaurant.objects.get(id=pk)
    if request.user.is_authenticated:
        if userIs(user.Customer) != True:
            return redirect('home-nexus')
        else:
            my_customer = user.Customer.objects.get(user=request.user)
            customer_status_info = restaurant.CustomerStatus.objects.filter(customer=my_customer).filter(restaurant=my_restaurant)
            if len(customer_status_info) > 0:
                customer_status_info = customer_status_info[0]
                status = customer_status_info.status
    recfood_order = restaurant.Order_Food.recomended(my_customer, my_restaurant) 
    recfood_popular = restaurant.Order_Food.popular(my_customer, my_restaurant)
    foods = restaurant.Food.objects.filter(cook__restaurant=my_restaurant)
    if request.method == "POST":
        if customer_status_info == None:
            customer_status_info = restaurant.CustomerStatus(customer=my_customer, restaurant=my_restaurant)
        status = 'P'
        customer_status_info.status = status
        customer_status_info.save()

    context = {
        'foods': foods,
        'orderRecFood': recfood_order,
        'popularRecFood': recfood_popular,
        'customer': my_customer,
        'restaurant': my_restaurant,
        'status': status
    }
    return render(request, "customer/restaurant.html", context=context)

def resturant_order(request, pk):
    userIs = userTypeChecker(request.user)
    my_restaurant = restaurant.Restaurant.objects.get(id=pk)
    my_customer = None
    customer_status_info = None
    status = 'N'
    my_restaurant = restaurant.Restaurant.objects.get(id=pk)
    if request.user.is_authenticated:
        if userIs(user.Customer) != True:
            return redirect('home-nexus')
        else:
            my_customer = user.Customer.objects.get(user=request.user)
            customer_status_info = restaurant.CustomerStatus.objects.filter(customer=my_customer).filter(restaurant=my_restaurant)
            if len(customer_status_info) > 0:
                customer_status_info = customer_status_info[0]
                status = customer_status_info.status
    foods = restaurant.Food.objects.filter(cook__restaurant=my_restaurant)
    
    if status == 'B':
        return redirect('home-nexus')

    if request.method == "POST":
        csr_token = 'csrfmiddlewaretoken'
        body = parse_req_body(request.body)
        my_order = restaurant.Order(restaurant=my_restaurant, customer=my_customer)
        my_order.save()
        total = 0
        for food_id_str in body:
            qty = body[food_id_str]
            if body != csr_token and qty > 0:
                food_id = int(food_id_str)
                myfood = restaurant.Food.objects.get(id=food_id)
                my_foodorder = restaurant.Order_Food(quantity=qty, order=my_order, food=myfood)
                my_foodorder.save()
                price = myfood.price 
                if status == 'V' and food.vip_free: 
                    price = 0
                total += price*qty
        discount = 0
        if status in ['V', 'R']:
            discount = 0.05
        total = total*(1-discount)
        my_order.total_price = total
        my_order.save()
    context = {
        'foods': foods,
        'restaurant': my_restaurant,
        'status': status
    }
    return render(request, "customer/restaurant_order.html", context=context)

def orders(request):
    context = {}
    return render(request, "customer/order.html", context=context) #html file will change
