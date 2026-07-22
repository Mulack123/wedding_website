from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from main.models import Music, Invite, Guest, RSVP
from django.utils import timezone

import pytest

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

class RsvpModelTest(TestCase):
    def setUp(self):
        self.invite = Invite.objects.create(name="Calum", code="test-code")
        self.guest = Guest.objects.create(
            name="Calum",
            invite=self.invite
        )
    
    def test_create_rsvp(self):
        rsvp = RSVP.objects.create(guest=self.guest, going=True)
        
        assert rsvp.id is not None
        assert rsvp.guest == self.guest
        assert rsvp.going is True
        
    def test_timestamp_is_auto_set(self):
        before = timezone.now()
        rsvp = RSVP.objects.create(guest=self.guest, going=True)
        after = timezone.now()

        assert rsvp.timestamp is not None
        assert before <= rsvp.timestamp <= after
        
    def test_custom_timestamp_is_respected(self):
        custom_time = timezone.now() - timezone.timedelta(days=1)

        rsvp = RSVP.objects.create(
            guest=self.guest,
            going=True,
            timestamp=custom_time
        )

        assert rsvp.timestamp == custom_time
        
    def test_one_to_one_constraint(self):
        RSVP.objects.create(guest=self.guest, going=True)

        with pytest.raises(IntegrityError):
            RSVP.objects.create(guest=self.guest, going=False)
            
    def test_cascade_delete(self):
        rsvp = RSVP.objects.create(guest=self.guest, going=True)

        self.guest.delete()

        assert RSVP.objects.filter(id=rsvp.id).count() == 0
        
    def test_string_representation_going(self):
        rsvp = RSVP.objects.create(guest=self.guest, going=True)

        assert str(rsvp) == f"{self.guest} is going"

    def test_string_representation_not_going(self):
        rsvp = RSVP.objects.create(guest=self.guest, going=False)

        assert str(rsvp) == f"{self.guest} is not going"

    def test_queryset_filter_going(self):
        invite1 = Invite.objects.create(name="Bob", code="test-code1")
        invite2 = Invite.objects.create(name="Alice", code="test-code2")
        
        guest1 = Guest.objects.create(name=invite1.name, invite=invite1)
        guest2 = Guest.objects.create(name=invite2.name, invite=invite2)

        RSVP.objects.create(guest=guest1, going=True)
        RSVP.objects.create(guest=guest2, going=False)

        going_guests = RSVP.objects.filter(going=True)

        assert going_guests.count() == 1
        assert going_guests.first().guest == guest1
        
    def test_queryset_filter_not_going(self):
        invite3 = Invite.objects.create(name="Ben", code="test-code3")
        invite4 = Invite.objects.create(name="Emily", code="test-code4")
        
        guest1 = Guest.objects.create(name=invite3.name, invite=invite3)
        guest2 = Guest.objects.create(name=invite4.name, invite=invite4)

        RSVP.objects.create(guest=guest1, going=True)
        RSVP.objects.create(guest=guest2, going=False)

        not_going = RSVP.objects.filter(going=False)

        assert not_going.count() == 1
        assert not_going.first().guest == guest2
    