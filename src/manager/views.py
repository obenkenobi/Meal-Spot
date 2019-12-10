from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from database.models.restaurant import *
from database.models.user import *
from helper import parse_req_body, userTypeChecker
# Create your views here.

def home(request):
    print('manager-home')
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(Manager) == True: # returns true if user is manager, else false
            print('rendering to manager-home')
            restaurant=Restaurant.objects.get(manager__user=user)
            context = {'restaurant':restaurant}
            return render(request, 'manager/home.html', context=context)
        else:
            print('redirecting to home')
            return redirect('home-nexus')
    except Exception as e:
        print(e)
        return redirect('home-nexus')
    except:
        import traceback
        traceback.print_exc()
        return redirect('home-nexus')

def restaurant(request):
    print('manager-restaurant')
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(Manager) == True: # returns true if user is manager, else false
            restaurant = Restaurant.objects.get(manager__user=user)
            if request.method == 'POST':
                body = parse_req_body(request.body)
                task = body['task']
                if task = "edit_name":
                    name = body['name']
                    restaurant.name = name

                elif task = "edit_description":
                    description = body['description']
                    restaurant.description = description
                
                restaurant.save()
                
            context = {'restaurant': restaurant}
            return render(request, 'manager/restaurant.html', context=context)
        else:
            print('user not manager')
            return redirect('home-nexus')
    except:
        import traceback
        traceback.print_exc()
        return redirect('home-nexus')

def deliverybids(request):
    print('manager-deliverybids')
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(Manager) == True:
            user_manager = Manager.objects.get(user=user)
            # at event that manager selects bid
            if request.method == 'POST':
                body = parse_req_body(request.body)
                task = body['task']
                if task = "choose_bid":
                    bid_id = int(body['bid_id'])
                    win_bid = DeliveryBid.objects.get(id=bid_id)
                    bid_order = win_bid.order
                    if bid_order.chose_bid == False:
                        win_bid.win = True
                        win_bid.save()
                        bid_order.chose_bid = True
                        bid_order.save()
            
            deliverybids_info = []
            orders = Order.objects.filter(restaurant=user_manager.restaurant, status='PR', chose_bid=False).order_by('created') 
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
        import traceback
        traceback.print_exc()
        return redirect('home-nexus')

def staff(request):
    #removewarnings,
    #view applications
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(Manager) == True:
            restaurant = Restaurant.objects.get(manager=user)

            if request.method == 'POST':
                body = parse_req_body(request.body)
                staff_id = body['staff_id'] #this is a user object, COULD CAUSE ERRORS
                staff_user = User.objects.get(pk=staff_id)
                update_staff = Staff.objects.get(user=staff_user) 
                staffIs = userTypeChecker(staff_user)
                task = body['task']
                if task = 'remove_warning':
                    if update_staff.warnings > 1:
                        update_staff.warnings -= 1
                
                elif task = 'fire':
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

                elif task = 'edit_salary':
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
        import traceback
        traceback.print_exc()
        return redirect('home-nexus')

def staffdetails(request, pk):
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(Manager) == True:
            staff_user = User.objects.get(pk=pk)
            staff = Staff.objects.get(user=staff_user) 
            staffIs = userTypeChecker(staff_user)

            if request.method == 'POST':
                body = parse_req_body(request.body)
                task = body['task']
                if task = 'remove_warning':
                    if staff.warnings > 1:
                        staff.warnings -= 1
                
                elif task = 'fire':
                    if staffIs(Cook): # check if there is enough cooks
                        if len(Cook.objects.filter(restaurant=restaurant)) > 2:
                            staff.status = 'N'
                            staff.restaurant = None
                            staff.warnings = 0
                            staff.salary = 0
                    elif staffIs(Salesperson): # check if there is enough salespeople
                        if len(Salesperson.objects.filter(restaurant=restaurant)) > 2:
                            staff.status = 'N'
                            staff.restaurant = None
                            staff.warnings = 0
                            staff.salary = 0                        
                    else:
                        staff.status = 'N'
                        staff.restaurant = None
                        staff.warnings = 0
                        staff.salary = 0

                elif task = 'edit_salary':
                    salary = body['salary']
                    staff.salary = salary

                staff.save()      

            if staffIs(Cook): 
                staff_type = "cook"
                complaints = Order_Food.filter(order__restaurant=restaurant).filter(food__cook=staff).filter(food_complaint__isnull=False)
                orders = Order_Food.filter(order__restaurant=restaurant).filter(food__cook=staff).order_by('-order__created') #not sure if order_by allows this

            elif staffIs(Deliverer):
                staff_type = "deliverer"
                complaints = Order.objects.filter(restaurant=restaurant).filter(deliverer=staff).filter(delivery_complaint__isnull=False)
                orders = Order.objects.filter(restaurant=restaurant).filter(deliverer=staff).order_by('-created')

            elif staffIs(Salesperson):
                staff_type = "salesperson"
                complaints = SupplyOrder.objects.filter(restaurant=restaurant).filter(salesperson=staff).filter(supply_complaint__isnull=False)
                orders = SupplyOrder.objects.filter(restaurant=restaurant).filter(salesperson=staff).order_by('-created')

            context = { 
                'staff': staff,
                'staff_type': staff_type,
                'complaints': complaints,
                'orders': orders,
            }
            return render(request, 'staffdetails.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        import traceback
        traceback.print_exc()
        return redirect('home-nexus')

def customers(request):
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(Manager) == True:
            restaurant = Restaurant.objects.get(manager=user)  
                 
            if request.method == 'POST':
                body = parse_req_body(request.body) 
                customer_id = int(body['customer_id'])  
                customer = User.objects.get(pk=customer_id)
                update_customer = CustomerStatus.objects.filter(restaurant=restaurant).filter(customer=customer)
                task = body['task']
                if task = "promote":
                    update_customer.status = 'V'
                elif task = "demote":
                    update_customer.status = 'R'                    
                elif task = "remove":
                    update_customer.status = 'N' 
                elif task = "blacklist":
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
        import traceback
        traceback.print_exc()
        return redirect('home-nexus')

def customerdetails(request, pk): #must send customerid
    try:
        user = request.user
        userIs = userTypeChecker(user)
        if userIs(Manager) == True:
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

            order_info = []
            orders = Order.objects.filter(restaurant=restaurant).filter(customer=customer).order_by('created')
            for order in orders:
                info_entry = {}
                info_entry['order'] = order
                total_items = sum(order.order_Food.quantity)
                info_entry['total_items'] = total_items
                order_info.append(info_entry) 
            
        
            food_complaints = Order_Food.objects.filter(customer=pk).filter(food_complaint__isnull=False)
            
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
            return render(request, 'customerdetails.html', context=context)
        else:
            return redirect('home-nexus')
    except:
        import traceback
        traceback.print_exc()
        return redirect('home-nexus')

def pendingregistrations(request): #if post, request must have customer user obj
# try:
#     user = request.user
#     userIs = userTypeChecker(user)
#     if userIs(Manager) == True:
    if request.method == 'POST':
        body = parse_req_body(request.body)
        user_id = int(body['user_id'])  #this is a user object, COULD CAUSE ERRORS
        update_user = User.objects.get(pk=user_id)
        task = body['task']

        if task = 'approve_customer':
            update_customer = CustomerStatus.objects.get(customer__user=update_user)
            update_customer.approve_status()
            update_customer.save()
        elif task = 'reject_customer':
            update_customer = CustomerStatus.objects.get(customer__user=update_user)
            update_customer.approve_status()  
            update_customer.save()  

        # change cook
        elif task = 'approve_cook':
            update_staff = Cook.objects.get(user=update_user) 
            update_staff.status = 'H'
            update_staff.salary = 600
            update_staff.save()
        elif task = 'reject_cook':
            update_staff = Cook.objects.get(user=update_user) 
            update_staff.status = 'N'
            update_staff.restaurant = None     
            update_staff.save()

        # change salesperson
        elif task = 'approve_salesperson':
            update_staff = Salesperson.objects.get(user=update_user) 
            update_staff.status = 'H'
            update_staff.salary = 600
            update_staff.save()
        elif task = 'reject_salesperson':
            update_staff = Salesperson.objects.get(user=update_user) 
            update_staff.status = 'N'
            update_staff.restaurant = None     
            update_staff.save()

        # change deliverer
        elif task = 'approve_deliverer':
            update_staff = Deliverer.objects.get(user=update_user) 
            update_staff.status = 'H'
            update_staff.salary = 600
            update_staff.save()
        elif task = 'reject_deliverer':
            update_staff = Deliverer.objects.get(user=update_user) 
            update_staff.status = 'N'
            update_staff.restaurant = None     
            update_staff.save()


        pending_customers = list(CustomerStatus.objects.filter(restaurant=restaurant).filter(status='P'))
        
        pending_cooks= list(Cook.objects.filter(restaurant=restaurant).filter(status='N'))
        pending_salespeople = list(Salesperson.objects.filter(restaurant=restaurant).filter(status='N'))
        pending_deliverers = list(Deliverer.objects.filter(restaurant=restaurant).filter(status='N'))
        
        context = { 
            'pending_customers': pending_customers,
            'pending_cooks':pending_cooks,
            'pending_salespeople':pending_salespeople,
            'pending_deliverers':pending_deliverers
        }
        return render(request, 'manager/pendingregistrations.html', context=context)            

    elif request.method == 'GET':
        user = request.user
        restaurant = Restaurant.objects.get(manager__user=user)
    
        pending_customers = list(CustomerStatus.objects.filter(restaurant=restaurant).filter(status='P'))
        
        pending_cooks= list(Cook.objects.filter(restaurant=restaurant).filter(status='N'))
        pending_salespeople = list(Salesperson.objects.filter(restaurant=restaurant).filter(status='N'))
        pending_deliverers = list(Deliverer.objects.filter(restaurant=restaurant).filter(status='N'))
        
        context = { 
            'pending_customers': pending_customers,
            'pending_cooks':pending_cooks,
            'pending_salespeople':pending_salespeople,
            'pending_deliverers':pending_deliverers
        }
        return render(request, 'manager/pendingregistrations.html', context=context)
    #     else:
    #         print('not manager')
    #         return redirect('home-nexus')
    # except:
    #     import traceback
    #     traceback.print_exc()
    #     return redirect('home-nexus')
