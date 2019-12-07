from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from database.models import user, restaurant, address
from helper import parse_req_body, userTypeChecker
import django.views

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
