from django.db import models
from django.utils import timezone

class Invite(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True, primary_key=True)

    def __str__(self):
        return self.name.__str__()

# Create your models here.
class Guest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    invite = models.ForeignKey(Invite, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.__str__()

class RSVP(models.Model):
    guest = models.OneToOneField(Guest, on_delete=models.CASCADE)
    going = models.BooleanField()
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.guest} is {'going' if self.going else 'a loser'}"
    #TODO: Food choice

class Music(models.Model):
    invite = models.ForeignKey(Invite, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    spotify_link = models.URLField(blank=True, help_text="If you can provide one it will be easier for us!")
    
    def __str__(self):
        return f"{self.title} by {self.artist}"
