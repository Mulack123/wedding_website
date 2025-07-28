from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from main.models import Guest

# Create your views here.
def home(request):
    guests = Guest.objects.all()
    return render(request, "main/index.html", {
        "title":"I&C Wedding",
        "guests":guests,
    })
