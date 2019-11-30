from django.shortcuts import render
from database.models.restaurant import *
# Create your views here.

class View:
    def pending_registrations(request):
        if request.method == 'GET':
            customers = CustomerStatus.objects.filter(status='P')


            pending_registrations = {
                'customers': customers,
                'order_history': order_history,
            }
            return render(request, 'pending_registrations.html', context=pending_registrations)

    #def delivery_bids(request):
        # view deliverybids, list in increasing order

        # model = Order
        # context_object_name = 'delivery_bids'
        # queryset = Order.objects.filter(status='PR')
        #
        # model = DeliveryBid
        # context_object_name = 'delivery_bids'
        # queryset = DeliveryBid.objects.filter(status='PR')

   # def manage_staff(request):
        #staff = Staff.objects.
        #hire, fire, remove warnings,
