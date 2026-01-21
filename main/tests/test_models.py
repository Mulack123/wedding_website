from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Music, Invite, Guest

# Create your tests here.
class MusicModelTest(TestCase):
    def setUp(self):
        self.invite = Invite.objects.create(name="Calum", code="test-code")
        self.music = Music.objects.create(
            invite=self.invite,
            title="test_title",
            artist="test_artist",
            spotify_link="https://open.spotify.com/track/example"
        )
    def test_music_object_creation(self):
        self.assertEqual(Music.objects.count(), 1)
    def test_spotify_link_blank(self):
        music = Music.objects.create(
            invite=self.invite,
            title="test_title",
            artist="test_artist"
        )
        self.assertEqual(music.spotify_link, "")

class GuestModelTest(TestCase):
    def setUp(self):
        self.invite = Invite.objects.create(name="Calum", code="test-code")
        self.guest = Guest.objects.create(
            name="Calum",
            invite=self.invite
        )
    def test_guest_object_creation(self):
        self.assertEqual(Guest.objects.count(), 1)
    
    def test_guest_name_unique(self):
        with self.assertRaises(IntegrityError):
            guest = Guest.objects.create(
            name="Calum",
            invite=self.invite
        )
            
class InviteModelTest(TestCase):
    def setUp(self):
        self.invite = Invite.objects.create(name="Calum", code="test-code")
    def test_invite_object_creation(self):
        self.assertEqual(Invite.objects.count(), 1)
    