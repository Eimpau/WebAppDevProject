from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question
from .forms import QuestionForm


def index(request):
    context = {}
    return render(request, "myapp/index.html", context)


