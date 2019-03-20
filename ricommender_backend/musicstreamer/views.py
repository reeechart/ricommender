import os

from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View

from rest_framework import generics
from rest_framework.views import APIView

from ricommender_backend.musicstreamer.models import Music
from ricommender_backend.musicstreamer.serializers import MusicSerializer

# Create your views here.

class MusicListView(generics.ListCreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

class MusicRetriever(View):
    @classmethod
    def get_music(cls, request, music_id):
        music_filepath = Music.objects.values_list('file', flat=True).get(pk=music_id)
        music_filepath = os.environ.get('MUSIC_DIRECTORY') + music_filepath
        if (request.method == 'GET'):
            try:
                music_file = open(music_filepath, 'rb')
                response = HttpResponse()
                response.streaming = True
                response.write(music_file.read())
                response['Content-Type'] = 'audio/mp3'
                response['Content-Length'] = os.path.getsize(music_filepath)
                return response
            except:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
