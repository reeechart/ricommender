import os

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View

from rest_framework import filters
from rest_framework import generics
from rest_framework.views import APIView

from ricommender_backend.musicstreamer.models import History
from ricommender_backend.musicstreamer.models import Music
from ricommender_backend.musicstreamer.recommender import MusicRecommendationCalculator
from ricommender_backend.musicstreamer.serializers import HistoryCreateSerializer
from ricommender_backend.musicstreamer.serializers import HistoryReadSerializer
from ricommender_backend.musicstreamer.serializers import MusicSearchSerializer
from ricommender_backend.musicstreamer.serializers import MusicSerializer

# Create your views here.

class MusicListView(generics.ListCreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

class MusicSearchView(generics.ListAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSearchSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title', )

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

class MusicRecommender(View):
    @classmethod
    def get_top_thirty_recommendation(cls, request):
        if (request.method == 'GET'):
            username = request.GET['user']
            location = request.GET['loc']
            weather = request.GET['weather']
            n = request.GET['n']
            all_history = History.objects.select_related('music__id', 'music__num_frames', 'music__frame_0', 'music__frame_1', 'music__frame_2', 'music__frame_3', 'music__frame_4', 'music__frame_5', 'music__frame_6').all()
            all_history = all_history.values('user', 'location', 'weather', 'music__id', 'music__num_frames', 'music__frame_0', 'music__frame_1', 'music__frame_2', 'music__frame_3', 'music__frame_4', 'music__frame_5', 'music__frame_6')
            all_music = Music.objects.values('id', 'file', 'title', 'artist', 'album')
            music_recommendation_calculator = MusicRecommendationCalculator(username, location, weather)
            recommendations = music_recommendation_calculator.get_top_n_recommendation(n, all_history, all_music)
            response = HttpResponse()
            response['Content-Type'] = 'application/json'
            response.write(recommendations)
            return response
        else:
            return HttpResponseNotAllowed("Method Not Allowed")

class HistoryCreateView(generics.CreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistoryCreateSerializer

class HistoryListView(generics.ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistoryReadSerializer
