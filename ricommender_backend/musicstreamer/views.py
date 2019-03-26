import os

from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View

from rest_framework import generics
from rest_framework.views import APIView

from ricommender_backend.musicstreamer.models import History
from ricommender_backend.musicstreamer.models import Music
from ricommender_backend.musicstreamer.serializers import HistoryCreateSerializer
from ricommender_backend.musicstreamer.serializers import HistoryReadSerializer
from ricommender_backend.musicstreamer.serializers import MusicSerializer

# Create your views here.

class MusicListView(generics.ListCreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

class MusicMetadataView(generics.RetrieveAPIView):
    queryset = Music.objects.all()
    lookup_field = 'id'
    serializer_class = MusicSerializer

class MusicRetriever(View):
    @classmethod
    def get_music(cls, request, music_id):
        if (request.method == 'GET'):
            try:
                music_filepath = Music.objects.values_list('file', flat=True).get(pk=music_id)
                music_filepath = os.environ.get('MUSIC_DIRECTORY') + music_filepath
                music_file = open(music_filepath, 'rb')
                response = HttpResponse()
                response.streaming = True
                response.write(music_file.read())
                response['Content-Type'] = 'audio/mp3'
                response['Content-Length'] = os.path.getsize(music_filepath)
                return response
            except:
                return HttpResponseNotFound("Not Found")
        else:
            return HttpResponseBadRequest("Invalid Method")

class HistoryCreateView(generics.CreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistoryCreateSerializer

class HistoryListView(generics.ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistoryReadSerializer
