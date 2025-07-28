from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.
def home(request):
    template = loader.get_template("main/index.html")
    return render(request, "main/index.html", {"name":"Calum"})
