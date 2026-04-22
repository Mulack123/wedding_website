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
    account = "isobelcalumwedding"
    container = "images"
    list_url = f"https://{account}.blob.core.windows.net/{container}?restype=container&comp=list"
    import urllib.request
    import xml.etree.ElementTree as ET
    try:
        with urllib.request.urlopen(list_url) as resp:
            tree = ET.parse(resp)
        ns = {"a": "http://schemas.microsoft.com/windowsazure"}
        blobs = tree.findall(".//a:Blob/a:Name", ns)
        if not blobs:
            blobs = tree.findall(".//Blob/Name")
        photo_urls = [
            f"https://{account}.blob.core.windows.net/{container}/{b.text}"
            for b in blobs
            if b.text and b.text.startswith("GBP-")
        ]
    except Exception:
        photo_urls = []
    return render(request, "main/gallery.html", {"title": "I&C | Gallery", "photos": photo_urls})

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

def registry(request):
    return render(request, "main/registry.html", {"title": "I&C | Registry"})

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
