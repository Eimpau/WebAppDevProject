from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone




def home(request):
    context = {}
    return render(request, "myapp/index.html", context)

def about(request):
    context = {}
    return render(request, "myapp/about.html", context)

def guide(request):
    context = {}
    return render(request, "myapp/guide.html", context)

def login(request):
    context = {}
    return render(request, "myapp/login.html", context)

def machines(request):
    context = {}
    return render(request, "myapp/machines.html", context)

def products(request):
    context = {}
    return render(request, "myapp/products.html", context)




