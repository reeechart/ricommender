from django.contrib.auth.models import User

from rest_framework import serializers

from ricommender_backend.musicstreamer.models import Music
from ricommender_backend.musicstreamer.models import History

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

class HistoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field = 'username',
        queryset = User.objects.all()
    )

    music = serializers.SlugRelatedField(
        slug_field = 'id',
        queryset = Music.objects.all()
    )

    class Meta:
        model = History
        exclude = ('id', )

class HistoryReadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field = 'username',
        queryset = User.objects.all()
    )

    music = MusicSerializer(read_only=True)

    class Meta:
        model = History
        exclude = ('id', )
