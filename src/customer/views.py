from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from database.models import user, restaurant, address
from helper import parse_req_body, userTypeChecker
import django.views

# helper functions
def order_rate(my_customer, body):
    order_id = int(body['orderId'])
    delivery_rating = int(body['ratedel'] if body['ratedel'] != None else 3)
    delivery_complaint = body.get('delcomp', '')
    food_rating = int(body['ratefood'] if body['ratefood'] != None else 3)
    food_complaint = body.get('foodcomp', '')

    myorder = restaurant.Order.objects.get(id=order_id)
    myorder.delivery_rating = delivery_rating
    myorder.delivery_complaint = delivery_complaint
    myorder.save()
    mydeliverer = None
    for bid in restaurant.DeliveryBid.objects.filter(order=myorder).filter(win = True):
        mydeliverer = bid.deliverer
        mydeliverer.add_rating(delivery_rating)
        mydeliverer.save()

    orderfoods = myorder.orderfoods
    for orderfood in orderfoods:
        # give it a rating
        orderfood.food_rating = food_rating
        orderfood.food_complaint = food_complaint
        orderfood.save()

        # do cook food drops stuff
        food = orderfood.food
        food.avg_rating = (food.avg_rating*food.num_ratings + food_rating)/(food.num_ratings + 1)
        food.num_ratings = food.num_ratings + 1
        food.save()
        cook = food.cook
        if food.avg_rating < 2:
            food.delete()
            cook.add_food_drops()
        cook.save()

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
    recfood_order = None
    my_restaurant = restaurant.Restaurant.objects.get(id=pk)
    if request.user.is_authenticated:
        if userIs(user.Customer) != True:
            return redirect('home-nexus')
        else:
            my_customer = user.Customer.objects.get(user=request.user)
            try:
                customer_status_info = restaurant.CustomerStatus.objects.filter(customer=my_customer).get(restaurant=my_restaurant)
                status = customer_status_info.status
            except:
                customer_status_info = restaurant.CustomerStatus(customer=my_customer, restaurant=my_restaurant)
                customer_status_info.status = status
                customer_status_info.save()
        recfood_order = restaurant.Order_Food.recomended(my_customer, my_restaurant) 
    recfood_popular = restaurant.Order_Food.popular(my_restaurant)
    foods = restaurant.Food.objects.filter(cook__restaurant=my_restaurant)
    if request.method == "POST":
        if customer_status_info == None:
            customer_status_info = restaurant.CustomerStatus(customer=my_customer, restaurant=my_restaurant)
        status = 'P'
        customer_status_info.status = status
        customer_status_info.save()

    print('status:',status)
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
            qty = 0
            try:
                qty = int(body[food_id_str])
            except:
                qty = 0
            if food_id_str != csr_token and qty > 0:
                food_id = int(food_id_str)
                myfood = restaurant.Food.objects.get(id=food_id)
                my_foodorder = restaurant.Order_Food(quantity=qty, order=my_order, food=myfood)
                my_foodorder.save()
                price = myfood.price 
                if status == 'V' and food.vip_free: 
                    price = 0
                total += price*qty
        discount = 0
        if status == 'V' or status == 'R':
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
    userIs = userTypeChecker(request.user)
    my_customer = None
    if request.user.is_authenticated:
        if userIs(user.Customer) != True:
            return redirect('home-nexus')
        else:
            my_customer = user.Customer.objects.get(user=request.user)
    else:
        return redirect('home-nexus')

    if request.method == "POST":
        body = parse_req_body(request.body)
        order_rate(my_customer, body)

    myorders = restaurant.Order.objects.filter(customer=my_customer)
    myorderdata = []
    for order in myorders:
        food_rating = restaurant.Order_Food.objects.filter(order=order)[0].food_rating
        data_entry = {
            'order': order,
            'description': order.food_description,
            'foodRating': food_rating,
        }
        myorderdata.append(data_entry)
    
    context = {
        'myorderdata': myorderdata
    }
    return render(request, "customer/order.html", context=context) #html file will change
