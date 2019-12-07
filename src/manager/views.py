from django.db import models
from django.shortcuts import render, redirect
from database.models.restaurant import *
from database.models.user import *
from helper import parse_req_body, userTypeChecker
# Create your views here.

def home(request):
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True: # returns true if user is manager, else false
            return render(request, 'manager-home.html')
        else:
            return redirect('home-nexus')
    except Exception as e:
        print(e)
        return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def restaurant(request):
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True: # returns true if user is manager, else false
            if request.method == 'POST':
                body = parse_req_body(request.body)
                name = body['name']
                description = body['description']
                current_user = request.user
                update_restaurant = Restaurant.objects.get(manager=current_user)
                update_restaurant.name = name
                update_restaurant.description = description
                update_restaurant.save()

            current_user = request.user
            restaurant = Restaurant.objects.get(manager=current_user)
            context = {'restaurant': restaurant}
            return render(request, 'manager/restaurant.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def deliverybids(request):
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            # at event that manager selects bid
            if request.method == 'POST':
                body = parse_req_body(request.body)
                chosen_bid = body['deliverybid']
                win_bid = DeliveryBid.objects.get(id=chosen_bid.id)
                win_bid.win = True
                win_bid.save()
                bid_order = win_bid.order
                order = Order.objects.get(id=bid_order.id)
                order.chose_bid = True
            
            deliverybids=[]
            orders = Orders.objects.filter(restaurant=restaurant_id, status='PR', chose_bid=False) #.order_by(order)
            for order in orders:
                order_bids={}
                bids = DeliveryBid.objects.filter(order=order).filter(won=False) #.order_by('price')
                order_bids[order] = bids
                deliverybid.append(order_bids)

            context = {
                'orders': orders,
                'deliverybids': deliverybids,
            }
            return render(request, 'manager/deliverybids.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def staff(request):
    #removewarnings,
    #view applications
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            if request.method == 'POST':
                body = parse_req_body(request.body)
                staff = body['staff']
                update_staff = Staff.objects.get(user=staff)

                if body['function'] == 'remove_warning':
                    update_staff.warnings -= 1
                
                elif body['function'] == 'fire':
                    update_staff.status = 'N'
                    update_staff.restaurant = None
                    update_staff.save()
                
                elif body['function'] == 'edit_salary':
                    salary = body['salary']
                    update_staff.salary = salary

                update_staff.save()        

            restaurant = Restaurant.objects.get(manager=user)
            staff = Staff.objects.filter(restaurant=restaurant, status='H')
            context = { 'staff': staff }
            return render(request, 'manager/staff.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def staffcomplaints(request):
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            body = parse_req_body(request.body)  
            staff = body['staff']
            if userIs(staff.Cook): 
                orders = Order.objects.filter(restaurant=restaurant).filter(cook=staff)
                complaints = []
                for order in orders:
                    order_complaints = Order_Food.filter(order = order).filter(food_complaint__isnull=False)
                    complaints.append(order_complaints)
            elif userIs(staff.Deliverer):
                complaints = Order.objects.filter(restaurant=restaurant).filter(deliverer=staff).filter(delivery_complaint__isnull=False)
            elif userIs(staff.Salesperson):
                complaints = SupplyOrder.objects.filter(restaurant=restaurant).filter(salesperson=salesperson).filter(supply_complaint__isnull=False)
            context = { 'complaints': complaints }
            return render(request, 'staffcomplaints.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def hirestaff(request):   
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            if request.method == 'POST':
                body = parse_req_body(request.body)
                staff = body['staff']
                update_staff = Staff.objects.get(user=staff)
                
                if body['function'] == 'hire':
                    update_staff.status = 'H'
                
                elif body['function'] == 'reject':
                    update_staff.status = 'N'
                    update_staff.restaurant = None
                
                update_staff.save()

            restaurant_id = Restaurant.objects.get(manager=user)
            pending_staff = Staff.objects.filter(restaurant=restaurant_id, status='N')
            context = { 'pending_staff': pending_staff }
            return render(request, 'hirestaff.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def customers(request):
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            restaurant = Restaurant.objects.get(manager=user)        
            if request.method == 'POST':
                body = parse_req_body(request.body)    
                customer = body['customer']

                update_customer = CustomerStatus.objects.filter(restaurant=restaurant).filter(user=customer)
                if body['function'] == 'promote':
                    update_customer.status = 'V'
                elif body['function'] == 'demote':
                    update_customer.status = 'R'                    
                update_customer.save()

            customers = CustomerStatus.objects.filter(restaurant=restaurant).order_by('avg_rating')
            context = { 'customers': customers }
            return render(request, 'customers.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def customercomplaints(request): #request must have customer obj
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            restaurant = Restaurant.objects.get(manager=user)
            body = parse_req_body(request.body) 
            customer = body['customer']  
            complaints = Order.objects.filter(restaurant=restaurant).filter(customer=customer).filter(customerrating__lte='2')
            context = { 'complaints': complaints }
            return render(request, 'customercomplaints.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def pendingregistrations(request): #if post, request must have customer obj
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            restaurant = Restaurant.objects.get(manager=user)
            if request.method == 'POST':
                body = parse_req_body(request.body)
                if body['function'] == 'accept':
                    update_customer = CustomerStatus.objects.get(pk=customer.id)
                    update_customer.approve_status()
                    update_customer.save()
                elif body['function'] == 'reject':
                    update_customer = CustomerStatus.objects.get(pk=customer.id)
                    update_customer.approve_status()  
                    update_customer.save()  
                elif body['function '] == 'remove':
                    update_customer.delete()

                customers = CustomerStatus.objects.filter(restaurant = restaurant, status='P')
                context = { 'customers': customers }
                return render(request, 'pendingregistrations.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')
