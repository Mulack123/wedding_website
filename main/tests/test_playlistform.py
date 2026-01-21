from django.test import TestCase
from main.models import Invite 
from main.forms import PlaylistForm

class PlaylistFormTestCase(TestCase):
    """
    Tests for the PlaylistForm
    1. Test valid form data
    2. Test invalid invite code
    3. Test invalid Spotify link
    4. Test empty Spotify link
    """

    def setUp(self):
        Invite.objects.create(name="Calum", code="ABC12")

    def test_valid_form(self):
        form_data = {
            'invite': 'ABC12',
            'title': 'Song Title',
            'artist': 'Artist Name',
            'spotify_link': 'https://open.spotify.com/track/1234567890'
        }
        form = PlaylistForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_break_everything(self):
        self.assertTrue(False)

    def test_invalid_invite_code(self):
        form_data = {
            'invite': 'INVALID',
            'title': 'Song Title',
            'artist': 'Artist Name',
            'spotify_link': 'https://open.spotify.com/track/1234567890'
        }
        form = PlaylistForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('invite', form.errors)

    def test_invalid_spotify_link(self):
        form_data = {
            'invite': 'ABC12',
            'title': 'Song Title',
            'artist': 'Artist Name',
            'spotify_link': 'https://invalidlink.com/track/1234567890'
        }
        form = PlaylistForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('spotify_link', form.errors)

    def test_empty_spotify_link(self):
        form_data = {
            'invite': 'ABC12',
            'title': 'Song Title',
            'artist': 'Artist Name',
            'spotify_link': ''
        }
        form = PlaylistForm(data=form_data)
        self.assertTrue(form.is_valid())
