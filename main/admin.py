from django.contrib import admin
from .models import Invite, Guest, RSVP, Music

# Register your models here.
admin.site.register([Invite, Guest, RSVP, Music])
