from django.shortcuts import render
from database.models.restaurant import *
# Create your views here.

def manager_home(request):
    if request.method == 'POST':
        #redirect to the link
    else:
       return render(request, 'manager_home.html')

def restaurant(request):
    if request.method == 'POST':
        # TODO
        # edit restaurant name
        # edit restaurant phonenumber
        # edit restaurant description
    else:
        return render(request, 'restaurant.html')

def delivery_bids(request, order_id):
    if request.method == 'POST':
        # delivery_bid chosen marked as DeliveryBid.won = True
        if order_id != null:
            lowest_bid = DeliveryBid.objects.get(order=order_id)
            lowest_bid.win = True
            lowest_bid.save()
            order = Order.objects.get(order=order_id)
            deliverer = lowest_bid.deliverer
            order.deliverer = deliverer
            order.save()
    else:
        # view deliverybids, list in increasing order
        delivery_bids = DeliveryBid.objects.filter(order=order_id).order_by('price')
        return render(request, 'delivery_bids.html', context=delivery_bids)

#TODO def staff(request):
    #staff = StaffStatus
    #hire, fire, remove warnings,
    #view applications

#TODO def customers(request):

#TODO def hire(request):

def pending_registrations(request):
    if request.method == 'POST':

    else:
        customers = CustomerStatus.objects.filter(status='P')
        return render(request, 'pending_registrations.html', context=customers)