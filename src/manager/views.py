from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
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
                if request.POST.get("choose_bid"):
                    body = parse_req_body(request.body)
                    bid_id = int(body['bid_id'])
                    win_bid = DeliveryBid.objects.get(id=bid_id)
                    bid_order = win_bid.order
                    if bid_order.chose_bid == False:
                        win_bid.win = True
                        win_bid.save()
                        bid_order.chose_bid = True
                        bid_order.save()
            
            deliverybids_info = []
            orders = Orders.objects.filter(restaurant=restaurant_id, status='PR', chose_bid=False) #.order_by(order)
            for order in orders:
                info_entry = {}
                bids = DeliveryBid.objects.filter(order=order).filter(won=False).order_by('price')
                info_entry['order'] = order
                info_entry['bids'] = bids
                deliverybids_info.append(info_entry)

            context = {
                'deliverybids_info': deliverybids_info,
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
            restaurant = Restaurant.objects.get(manager=user)

            if request.method == 'POST':
                body = parse_req_body(request.body)
                staff_id = body['staff_id'] #this is a user object, COULD CAUSE ERRORS
                staff_user = User.objects.get(pk=staff_id)
                update_staff = Staff.objects.get(user=staff_user) 
                staffIs = userTypeChecker(staff_user)

                if request.POST.get('remove_warning'):
                    if update_staff.warnings > 1:
                        update_staff.warnings -= 1
                
                elif request.POST.get('fire'):
                    if staffIs(Cook): # check if there is enough cooks
                        if len(Cook.objects.filter(restaurant=restaurant)) > 2:
                            update_staff.status = 'N'
                            update_staff.restaurant = None
                            update_staff.warnings = 0
                            update_staff.salary = 0
                    elif staffIs(Salesperson): # check if there is enough salespeople
                        if len(Salesperson.objects.filter(restaurant=restaurant)) > 2:
                            update_staff.status = 'N'
                            update_staff.restaurant = None
                            update_staff.warnings = 0
                            update_staff.salary = 0                        
                    else:
                        update_staff.status = 'N'
                        update_staff.restaurant = None
                        update_staff.warnings = 0
                        update_staff.salary = 0

                elif request.POST.get('edit_salary'):
                    salary = body['salary']
                    update_staff.salary = salary

                update_staff.save()        
            
            staff = Staff.objects.filter(restaurant=restaurant, status='H')
            cooks = []
            salespeople = []
            deliverers = []
            for member in staff:
                member_user = member.user
                staffIs = userTypeChecker(member_user)
                if staffIs(Cook):
                    cooks.append(member)
                elif staffIs(Salesperson):
                    salespeople.append(member)            
                if staffIs(Deliverer):
                    deliverers.append(member)            
            context = { 
                'cooks': cooks,
                'salespeople': salespeople,
                'deliverers': deliverers,
            }
            return render(request, 'manager/staff.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def staff_details(request, pk):
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            staff = Staff.objects.get(user=pk)
            if userIs(staff.Cook): 
                orders = Order.objects.filter(restaurant=restaurant).filter(cook=staff)
                complaints = []
                for order in orders:
                    order_complaints = Order_Food.filter(order = order).filter(food_complaint__isnull=False)
                    complaints.append(order_complaints)
            elif userIs(staff.Deliverer):
                complaints = Order.objects.filter(restaurant=restaurant).filter(deliverer=staff).filter(delivery_complaint__isnull=False)
            elif userIs(staff.Salesperson):
                complaints = SupplyOrder.objects.filter(restaurant=restaurant).filter(salesperson=staff).filter(supply_complaint__isnull=False)
            context = { 'complaints': complaints }
            return render(request, 'staff_details.html', context=context)
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
                customer_id = int(body['customer_id'])  
                customer = User.objects.get(pk=customer_id)
                update_customer = CustomerStatus.objects.filter(restaurant=restaurant).filter(customer=customer)
                if request.POST.get("promote"):
                    update_customer.status = 'V'
                elif request.POST.get("demote"):
                    update_customer.status = 'R'                    
                elif request.POST.get("remove"):
                    update_customer.status = 'N' 
                elif request.POST.get("blacklist"):
                    update_customer.status = 'B'                     
                update_customer.save()
            
            registered_customers = CustomerStatus.objects.filter(restaurant=restaurant).order_by('avg_rating')
            customer_info = []
            for registered_customer in registered_customers:
                info_entry = {}
                info_entry['registered_customer'] = registered_customer
                complaintcount = len(Order.objects.filter(restaurant=restaurant).filter(customer=customer).filter(customerrating__lte='2'))
                info_entry['complaintcount'] = complaintcount
                customer_info.append(info_entry) 

            context = { 
                'customer_info': customer_info
            }
            return render(request, 'customers.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def customer_details(request, pk): #must send customerid
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            restaurant = Restaurant.objects.get(manager=user) 
            customer = get_object_or_404(User, pk=pk)
            if request.method == 'POST':
                body = parse_req_body(request.body)    
                update_customer = CustomerStatus.objects.filter(restaurant=restaurant).filter(customer=customer)
                if body['function'] == 'promote':
                    update_customer.status = 'V'
                elif body['function'] == 'demote':
                    update_customer.status = 'R'                    
                elif body['function'] == 'remove':
                    update_customer.status = 'N' 
                elif body['function'] == 'blacklist':
                    update_customer.status = 'B'                     
                update_customer.save()

    # info_entry['registered_customer'] = registered_customer
    # complaintcount = len(Order.objects.filter(restaurant=restaurant).filter(customer=customer).filter(customerrating__lte='2'))
    # info_entry['complaintcount'] = complaintcount
    # customer_info.append(info_entry) 


            order_info = []
            orders = Order.objects.filter(restaurant=restaurant).filter(customer=customer)
            for order in orders:
                info_entry = {}
                info_entry['order'] = order
                total_items = sum(order.order_Food.quantity)
                info_entry['total_items'] = total_items
                order_info.append(info_entry) 
            
        
            food_complaints = Order_Food.objects.filter(customer=pk).filter(food_complaint__isnull=False))
            
            delivery_complaints = Order.objects.filter(restaurant=restaurant).filter(customer=pk).filter(delivery_rating__lte='2')

            complaints_received = Order.objects.filter(restaurant=restaurant).filter(customer=pk).filter(customer_rating__lte='2')
            num_complaints = len(complaints_received)
            context = { 
                'customer': customer,
                'num_complaints': num_complaints,
                'complaints_received': complaints_received, 
                'food_complaints': food_complaints,
                'delivery_complaints': delivery_complaints,
                'orders': orders_info,
            }
            return render(request, 'customer_details.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')

def pendingregistrations(request): #if post, request must have customer user obj
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(user.Manager) == True:
            restaurant = Restaurant.objects.get(manager=user)
            if request.method == 'POST':
                body = parse_req_body(request.body)
                user_id = int(body['user_id'])  #this is a user object, COULD CAUSE ERRORS
                update_user = User.objects.get(pk=user_id)
                if request.POST.get('approve_customer'):
                    update_customer = CustomerStatus.objects.get(customer=update_user)
                    update_customer.approve_status()
                    update_customer.save()
                elif request.POST.get('reject_customer'):
                    update_customer = CustomerStatus.objects.get(customer=update_user)
                    update_customer.approve_status()  
                    update_customer.save()  
                elif request.POST.get('approve_staff'):
                    update_staff = Staff.objects.get(user=update_user) 
                    update_staff.status = 'H'
                    update_staff.salary = 600
                    update_staff.save()
                elif request.POST.get('reject_staff'):
                    update_staff = Staff.objects.get(user=update_user) 
                    update_staff.status = 'N'
                    update_staff.restaurant = None     
                    update_staff.save()
            
            pending_customers = CustomerStatus.objects.filter(restaurant = restaurant, status='P')
            
            pending_staff = Staff.objects.filter(restaurant=restaurant, status='N')

            pending_staff_info = []
            
            for staff in pending_staff:
                info_entry = {}
                staffIs = userTypeChecker(staff)
                info_entry['staff'] = staff
                if staffIs(Cook):
                    info_entry['staff_type'] = "Cook"
                elif staffIs(Deliverer):
                    info_entry['staff_type'] = "Deliverer"                    
                elif staffIs(Salesperson):
                    info_entry['staff_type'] = "Salesperson"
                pending_staff_info.append(info_entry)
                
            context = { 
                'pending_customers': pending_customers,
                'pending_staff_info': pending_staff_info
            }
            return render(request, 'pendingregistrations.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        return redirect('home-nexus')
