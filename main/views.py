from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.
def home(request):
    return render(request, "main/index.html", {"title":"I&C Wedding"})

def details(request):
    return render(request, "main/details.html", {"title":"I&C Wedding"})
