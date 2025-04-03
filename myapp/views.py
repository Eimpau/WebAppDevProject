from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone




def home(request):
    context = {}
    return render(request, "myapp/Home.html", context)

def about(request):
    context = {}
    return render(request, "myapp/AboutUs.html", context)

def guide(request):
    context = {}
    return render(request, "myapp/Guide.html", context)

def login(request):
    context = {}
    return render(request, "myapp/Login.html", context)

def machineDescription(request):
    context = {}
    return render(request, "myapp/MachineDescription.html", context)

def products(request):
    context = {}
    return render(request, "myapp/Products.html", context)




