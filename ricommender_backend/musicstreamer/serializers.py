from rest_framework import serializers

from ricommender_backend.musicstreamer.models import Music

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'album')
