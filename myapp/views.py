from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import UserProfile
from .forms import LoginForm, ManagerUserRegistrationForm

def home(request):
    context = {}
    return render(request, "myapp/index.html", context)

def about(request):
    context = {}
    return render(request, "myapp/about.html", context)

def guide(request):
    context = {}
    return render(request, "myapp/guide.html", context)

def employee_login(request):
    if request.method == "POST":
        # Handle the login logic here
        # For example, authenticate the user and redirect to a different page
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Valid login
                login(request, user)
                return redirect("myapp:home") # to be changed to the employee page later
            else:
                # Invalid login
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    context = {'form': form,}
    return render(request, "myapp/login.html", context)

def machines(request):
    context = {}
    return render(request, "myapp/machines.html", context)

def products(request):
    context = {}
    return render(request, "myapp/products.html", context)

@login_required # Ensure the user is logged in before accessing this view
def employee_logout(request):
    logout(request)
    return redirect("myapp:home")

@login_required # Ensure the user is logged in before accessing this view
def manager_dashboard(request):
    if request.method == "POST":
        form = ManagerUserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the new user and their profile
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
                )
            UserProfile.objects.create(
                user=user, 
                role=form.cleaned_data['role']
                )
            return redirect("myapp:manager_dashboard")
    else:
        form = ManagerUserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, "myapp/manager_dashboard.html", context)

@login_required
def technician_dashboard(request):
    context = {}
    return render(request, "myapp/technician_dashboard.html", context)

@login_required
def repair_dashboard(request):
    context = {}
    return render(request, "myapp/repair_dashboard.html", context)

@login_required
def viewonly_dashboard(request):
    context = {}
    return render(request, "myapp/viewonly_dashboard.html", context)

