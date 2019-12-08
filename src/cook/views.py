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
        if userIs(user.Cook) != True:
            response = redirect('home-nexus')
            return response
    except Exception as e:
        print(e)
        response = redirect('home-nexus')
        return response
    except:
        response = redirect('home-nexus')
        return response
  
    my_cook = user.Cook.objects.get(user=my_user)
    
    registered = len(user.Cook.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_cook.status == 'H'

    if registered != True: # if not registered
        return redirect('cook-register')  
    
    if request.method == "POST":
        pass

    return render(request, 'cook/home.html', context={})

def register(request):
    my_user = None
    try:
        my_user = request.user
        isType = userTypeChecker(my_user)
        if isType(user.Cook) != True:
            response = redirect('home-nexus')
            return response
    except:
        response = redirect('home-nexus')
        return response

    my_cook = user.Cook.get(user=my_user)
    registered = len(user.Cook.objects.filter(user=my_user).exclude(restaurant__isnull=True)) > 0 and my_cook.status == 'H'
    if registered:
        return redirect('cook-home')
    registering = len(user.Cook.objects.filter(user=my_user).exclude(restaurant__isnull=False)) > 0 and my_cook.status != 'H'

    restaurants = restaurant.Restaurant.objects.all()
    context={'restaurants': restaurants, 'registering': registering}

    if registering != True and request.method == "POST":
        body = parse_req_body(request.body)
        resturant_id = int(body['id'])
        reg_resturant = restaurant.Restaurant.objects.get(id=resturant_id)
        my_cook.update(restaurant = reg_resturant)
        context['registering'] = True
    return render(request, 'cook/register.html', context={})