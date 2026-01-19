from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import PlaylistForm
from .models import Invite, Music

# Create your views here.
def home(request):
    return render(request, "main/index.html", {"title":"I&C Wedding"})

def details(request):
    return render(request, "main/details.html", {"title":"I&C | Details"})

def gallery(request):
    return render(request, "main/gallery.html", {"title":"I&C | Gallery"})

def playlist(request):
    # Get current song list
    current_playlist = Music.objects.all()
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            # Validated Data
            data = form.cleaned_data

            # Create record
            music = Music(
                invite=Invite.objects.get(code=data['invite']),
                title=data['title'],
                artist=data['artist'],
                spotify_link=data['spotify_link']
            )
            music.save()

            return render(request, "main/playlist_submitted.html", {"title":"I&C | Playlist", "playlist": current_playlist, "code": data['invite']})
            # return HttpResponseRedirect(f"/playlist/submitted?code={data['invite']}")
    else:
        code = request.GET.get("code")
        if code:
            # New form request
            form = PlaylistForm(initial={"invite": code})
        else: 
            form = PlaylistForm()

    return render(request, "main/playlist.html", {"title":"I&C | Playlist", "form":form, "playlist": current_playlist})
