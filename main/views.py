from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import PlaylistForm

# Create your views here.
def home(request):
    return render(request, "main/index.html", {"title":"I&C Wedding"})

def details(request):
    return render(request, "main/details.html", {"title":"I&C | Details"})

def gallery(request):
    return render(request, "main/gallery.html", {"title":"I&C | Gallery"})

def playlist(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/playlist/submitted")
    else:
        form = PlaylistForm()
    return render(request, "main/playlist.html", {"title":"I&C | Playlist", "form":form})
