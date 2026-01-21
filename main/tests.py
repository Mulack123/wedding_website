from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Music, Invite

# Create your tests here.
class MusicModelTest(TestCase):
    def setUp(self):
        self.invite = Invite.objects.create(name="Calum", code="test-code")
    def test_spotify_link_blank(self):
        music = Music.objects.create(
            invite=self.invite,
            title="test_title",
            artist="test_artist"
        )
        self.assertEqual(music.spotify_link, "")