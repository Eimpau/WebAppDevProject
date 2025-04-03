from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone




def home(request):
    context = {}
    return render(request, "myapp/Home.html", context)


