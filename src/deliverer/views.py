from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from database.models import user, restaurant, address
from helper import parse_req_body, userTypeChecker
import django.views

# Create your views here.

def home(request):
    my_user = None
    # makes sure user is deliverer
    try:
        my_user = request.user
        userIs = userTypeChecker(my_user)
        if userIs(user.Deliverer) != True:
            response = redirect('home-nexus')
            return response
    except Exception as e:
        print(e)
        response = redirect('home-nexus')
        return response
    except:
        response = redirect('home-nexus')
        return response

    my_deliverer = user.Deliverer.objects.get(user=my_user)
    
    registered = len(user.Deliverer.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_deliverer.status == 'H'

    if registered != True: # if not registered
        return redirect('deliverer-register')

    if request.method == "POST": # If bidded
        body = parse_req_body(request.body)
        amount = body['amount']
        order_id = body['orderId']
        order = restaurant.Order.get(id=order_id)
        new_bid = restaurant.DeliveryBid(deliverer=my_deliverer, win=False, price=amount, order=order)
        new_bid.save()
    open_bids = restaurant.DeliveryBid.objects.filter(deliverer__isnull=True).filter(order__restaurant = my_deliverer.restaurant)
    pending_bids = restaurant.DeliveryBid.objects.filter(deliverer=my_deliverer).filter(win=False)
    won_bids = restaurant.DeliveryBid.objects.filter(deliverer=my_deliverer).filter(win=True)
    context = {
        'warnings': my_deliverer.warnings,
        'openBids': open_bids,
        'pendingBids': pending_bids,
        'winningBids': won_bids
    }
    return render(request, 'deliverer/home.html', context=context)


def register(request):
    my_user = None
    try:
        my_user = request.user
        isType = userTypeChecker(my_user)
        if isType(user.Deliverer) != True:
            response = redirect('home-nexus')
            return response
    except:
        response = redirect('home-nexus')
        return response

    my_deliverer = user.Deliverer.get(user=my_user)
    registered = len(user.Deliverer.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_deliverer.status == 'H'
    if registered:
        return redirect('deliverer-home')
    registering = len(user.Deliverer.objects.filter(user=my_user).exclude(restaurant__isnull=False)) > 0 and my_deliverer.status != 'H'

    restaurants = restaurant.Restaurant.objects.all()
    context={'restaurants': restaurants, 'registering': registering}

    if registering != True and request.method == "POST":
        body = parse_req_body(request.body)
        resturant_id = int(body['id'])
        reg_resturant = restaurant.Restaurant.objects.get(id=resturant_id)
        my_deliverer.update(restaurant = reg_resturant)
        context['registering'] = True
    return render(request, 'deliverer/register.html', context=context)

def order(request, pk):
    order = get_object_or_404(restaurant.Order, pk=pk)
    customer = order.customer
    customer_address = address.CustomerAddress.get(customer=customer)

    my_resturant = user.Deliverer.get(user=my_user).restaurant
    restaurant_address = address.RestaurantAddress.get(restaurant=restaurant)

    if(request.method == "POST"):
        body = parse_req_body(request.body)
        rating = int(body['rating'])
        if 0 <= rating or rating <= 5:
            order.status = 'D'
            order.customer_rating = rating
            customer_status = restaurant.CustomerStatus.get(customer=customer, restaurant=my_resturant)
            customer_status.update_status(rating)
            order.save()
    rating = order.delivery_rating
    return render(request, 'deliverer/order.html', context={
        'order': order,
        'customerAddress': customer_address, 
        'restaurantAddress': restaurant_address
    })