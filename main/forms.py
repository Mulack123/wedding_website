from django import forms
import re
from .models import Invite

class PlaylistForm(forms.Form):
    invite = forms.CharField(label="Invite Code")
    title = forms.CharField(label="Title")
    artist = forms.CharField(label="Artist")
    spotify_link = forms.URLField(label="Spotify Link", required=False)

    def clean_invite(self):
        code = self.cleaned_data.get('invite')
        if not Invite.objects.filter(code=code).exists():
            raise forms.ValidationError("Invite code invalid")
        return  code



    def clean_spotify_link(self):
        spotify_link = self.cleaned_data.get('spotify_link')
        if not re.match(r'^(https:\/\/)?open\.spotify\.com\/track\/[A-Za-z0-9]+(\?.*)?$', spotify_link):
            raise forms.ValidationError("Enter a valid open.spotify.com link")
        return spotify_link

