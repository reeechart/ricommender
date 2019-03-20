from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Music(models.Model):
    file = models.CharField(_('File'), max_length=255)
    title = models.CharField(_('Title'), max_length=255)
    artist = models.CharField(_('Artist'), max_length=255)
    album = models.CharField(_('Album'), max_length=255)
