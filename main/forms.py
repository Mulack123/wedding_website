from django import forms

class PlaylistForm(forms.Form):
    invite = forms.CharField(label="Invite Code")
    title = forms.CharField(label="Title")
    artist = forms.CharField(label="Artist")
    spotify_link = forms.URLField(label="Spotify Link", required=False)