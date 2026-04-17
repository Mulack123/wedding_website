from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from .forms import PlaylistForm, RSVPCodeForm
from .models import Invite, Music, Guest, RSVP

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

def rsvp(request):
    if request.method == "POST":
        step = request.POST.get('step')
        if step == 'code':
            form = RSVPCodeForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect(f"/rsvp/?code={form.cleaned_data['code']}")
            return render(request, "main/rsvp_code.html", {"title": "I&C | RSVP", "form": form})
        elif step == 'rsvp':
            code = request.POST.get('code')
            try:
                invite = Invite.objects.get(code=code)
            except Invite.DoesNotExist:
                return HttpResponseRedirect('/rsvp/')
            guests = Guest.objects.filter(invite=invite)
            for guest in guests:
                going = request.POST.get(f'going_{guest.id}') == 'yes'
                dietary = request.POST.get(f'dietary_{guest.id}', '')
                RSVP.objects.update_or_create(
                    guest=guest,
                    defaults={'going': going, 'dietary_requirements': dietary, 'timestamp': timezone.now()}
                )
            return render(request, "main/rsvp_submitted.html", {"title": "I&C | RSVP", "invite": invite, "guests": guests})
    else:
        code = request.GET.get('code')
        if code:
            try:
                invite = Invite.objects.get(code=code)
                guests = Guest.objects.filter(invite=invite)
                return render(request, "main/rsvp.html", {"title": "I&C | RSVP", "invite": invite, "guests": guests, "code": code})
            except Invite.DoesNotExist:
                pass
        form = RSVPCodeForm()
        return render(request, "main/rsvp_code.html", {"title": "I&C | RSVP", "form": form})
