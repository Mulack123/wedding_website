from django.db import models
from django.utils import timezone

# Create your models here.
class Guest(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class RSVP(models.Model):
    guest = models.OneToOneField(Guest, on_delete=models.CASCADE, primary_key=True)
    going = models.BooleanField()
    timestamp = models.DateTimeField(default=timezone.now)
    #TODO: Food choice

# TODO: Decide on structure for Music suggestions
# class Music(models.Model):
#     guest = models.ForeignKey(Guest, on_delete="cascade")
#     title = models.CharField(max_length=100)
#     artist = models.CharField(max_length=100)
