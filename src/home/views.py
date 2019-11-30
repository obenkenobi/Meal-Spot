from django.shortcuts import render

# Create your views here.

def nexus(request):
    """
        This view will simply redirect the user to another
        url based on what usertype they are
    """
    return render(request, 'home/index.html', context={}) # rendering index.html for testing

