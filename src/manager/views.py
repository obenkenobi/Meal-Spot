from django.db import models
from django.shortcuts import render, redirect
from database.models.restaurant import *
from database.models.user import *
from helper import parse_req_body
# Create your views here.

def home(request):
    if request.method == 'POST':
        # redirect to the links?
        if request.path == 'restaurant':
            return redirect('restaurant')
        elif request.path == 'delivery_bids':
            return redirect('delivery_bids')
        elif request.path == 'staff':
            return redirect('staff')
        elif request.path == 'customers':
            return redirect('customers')
        elif request.path == 'hire':
            return redirect('hire')
        elif request.path == 'pending_registrations':
            return redirect('pending_registrations')
    else:
       return render(request, 'manager-home.html')

def restaurant(request):
    if request.method == 'POST':
        body = parse_req_body(request.body)
        name = body['name']
        phonenumber = body['phonenumber']
        description = body['description']
        current_user = request.user
        update_restaurant = Restaurant.objects.get(manager=current_user)
        update_restaurant.name = name
        update_restaurant.phonenumber = phonenumber
        update_restaurant.description = description
        update_restaurant.save()

    current_user = request.user
    restaurant = Restaurant.objects.get(manager=current_user)
    context = {'restaurant': restaurant}
    return render(request, 'manager/restaurant.html', context=context)


def delivery_bids(request):
    # at event that manager selects bid
    if request.method == 'POST':
        lowest_bid = DeliveryBid.objects.get(pk=delivery_bid_id)
        lowest_bid.win = True
        lowest_bid.save()
        order_id = lowest_bid.order
        order = Order.objects.get(pk=order_id)
        order.chose_bid = True

    prepared_orders = Orders.objects.filter(status='PR',chose_bid=False) #.order_by(order)
    delivery_bids = DeliveryBid.objects.filter(won=False) #.order_by('price')
    context = {
        'prepared_orders': prepared_orders,
        'delivery_bids': delivery_bids,
    }
    return render(request, 'manager/delivery_bids.html', context=context)

def staff(request, staff_id):
    #removewarnings,
    #view applications
    if request.method == 'POST':
        update_staff = Staff.objects.get(user=staff_id)
        update_staff.warnings -= 1
        update_staff.save()

    current_user = request.user
    restaurant_id = Restaurant.objects.get(manager=current_user)
    staff = Staff.objects.filter(restaurant=restaurant_id, status='H')
    context = { 'staff': staff }
    return render(request, 'manager/staff.html', context=context)

def hire_staff(request, staff_id):   
    if request.method == 'POST':
        update_staff = Staff.objects.get(user=staff_id)
        
        if request.body == 'hire':
            update_staff.status = 'H'
        
        elif request.body == 'reject':
            update_staff.status = 'N'
            update_staff.restaurant = None
        
        update_staff.save()
        
    current_user = request.user
    restaurant_id = Restaurant.objects.get(manager=current_user)
    pending_staff = Staff.objects.filter(restaurant=restaurant_id, status='N')
    context = { 'pending_staff': pending_staff }
    return render(request, 'hire_staff.html', context=context)

def customers(request, customer_id):
    if request.method == 'POST':
        update_customer = CustomerStatus.objects.get(user=customer_id)
        update_customer.warnings -= 1
        update_customer.save()

    current_user = request.user
    restaurant_id = Restaurant.objects.get(manager=current_user)
    customers = CustomerStatus.objects.filter(restaurant=restaurant_id)
    context = { 'customers': customers }
    return render(request, 'customers.html', context=context)

def pending_registrations(request, customer_id):
    if request.method == 'POST':
        customer_status = CustomerStatus.objects.get(pk=customer_id)
        customer_status.approve_status()
        customer_status.save()

    customers = CustomerStatus.objects.filter(status='P')
    context = { 'customers': customers }
    return render(request, 'pending_registrations.html', context=context)