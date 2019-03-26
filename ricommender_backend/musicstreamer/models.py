from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Music(models.Model):
    file = models.CharField(_('File'), max_length=255)
    title = models.CharField(_('Title'), max_length=255)
    artist = models.CharField(_('Artist'), max_length=255)
    album = models.CharField(_('Album'), max_length=255)
    tempo = models.FloatField(_('Tempo'), default=0)
    num_frames = models.IntegerField(_('Number of Frames'), default=0)
    frame_0 = models.IntegerField(_('Frame 0'), default=0)
    frame_1 = models.IntegerField(_('Frame 1'), default=0)
    frame_2 = models.IntegerField(_('Frame 2'), default=0)
    frame_3 = models.IntegerField(_('Frame 3'), default=0)
    frame_4 = models.IntegerField(_('Frame 4'), default=0)
    frame_5 = models.IntegerField(_('Frame 5'), default=0)
    frame_6 = models.IntegerField(_('Frame 6'), default=0)

class History(models.Model):
    OFFICE = 'office'
    GYM = 'gym'
    CANTEEN = 'canteen'
    LIBRARY = 'library'
    TRAVEL = 'travel'

    LOCATION_CHOICES = (
        (OFFICE, _('office')),
        (GYM, _('gym')),
        (CANTEEN, _('canteen')),
        (LIBRARY, _('library')),
        (TRAVEL, _('travel')),
    )

    SUNNY = 'sunny'
    CLOUDY = 'cloudy'
    RAIN = 'rain'

    WEATHER_CHOICES = (
        (SUNNY, _('sunny')),
        (CLOUDY, _('cloudy')),
        (RAIN, _('rain')),
    )

    user = models.ForeignKey(User, related_name='history', on_delete=models.CASCADE)
    location = models.CharField(_('Location'), max_length=64, choices=LOCATION_CHOICES)
    weather = models.CharField(_('Weather'), max_length=64, choices=WEATHER_CHOICES)
    music_rank = models.IntegerField(_('Music Rank'), default=0)
    music = models.ForeignKey(Music, related_name='history', on_delete=models.CASCADE)
