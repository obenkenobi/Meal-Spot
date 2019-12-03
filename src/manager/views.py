from django.shortcuts import render, redirect
from database.models.restaurant import *
# Create your views here.

def manager_home(request):
    if request.method == 'POST':
        #redirect to the link
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

# def restaurant(request):
#     if request.method == 'POST':
#         # TODO
#         # edit restaurant name
#         # edit restaurant phonenumber
#         # edit restaurant description
#     else:
#         return render(request, 'restaurant.html')

def delivery_bids(request, order_id):
    if request.method == 'POST':
        # delivery_bid chosen marked as DeliveryBid.won = True
        # get order_id idk how
        lowest_bid = DeliveryBid.objects.get(order=order_id)
        lowest_bid.win = True
        lowest_bid.save()
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

# def pending_registrations(request):
#     if request.method == 'POST':
#
#     else:
#         customers = CustomerStatus.objects.filter(status='P')
#         return render(request, 'pending_registrations.html', context=customers)