from django.contrib.auth.models import User
from django.shortcuts import render

from ricommender_backend.authentication.serializers import UserSerializer

from ricommender_backend.musicstreamer.models import History
from ricommender_backend.musicstreamer.models import Music

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView

# Create your views here.

class UserLoginView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = super().perform_create(serializer)
        user_model = User.objects.get(username=self.request.data['username'])
        musics = Music.objects.all().order_by('id')
        for location in History.LOCATION_LIST:
            for weather in History.WEATHER_LIST:
                for music in musics:
                    history = History(user=user_model, location=location, weather=weather,
                        music_rank=0, music=music)
                    history.save()
        return user

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
