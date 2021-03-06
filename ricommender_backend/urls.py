"""ricommender_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ricommender_backend.authentication.views import UserDeleteView
from ricommender_backend.authentication.views import UserLoginView
from ricommender_backend.authentication.views import UserRegisterView
from ricommender_backend.musicstreamer.views import HistoryCreateView
from ricommender_backend.musicstreamer.views import HistoryListView
from ricommender_backend.musicstreamer.views import MusicListView
from ricommender_backend.musicstreamer.views import MusicMetadataView
from ricommender_backend.musicstreamer.views import MusicRecommender
from ricommender_backend.musicstreamer.views import MusicRetriever
from ricommender_backend.musicstreamer.views import MusicSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login/<slug:username>', UserLoginView.as_view(), name='user-login'),
    path('user/delete/<slug:username>', UserDeleteView.as_view(), name='user-delete'),
    path('user/register', UserRegisterView.as_view(), name='user-register'),
    path('music/metadata/<slug:id>', MusicMetadataView.as_view(), name='music-metadata'),
    path('music/recommendation', MusicRecommender.get_top_thirty_recommendation, name='music-recommendation'),
    path('music/search', MusicSearchView.as_view(), name='music-search'),
    path('music/stream/<music_id>', MusicRetriever.get_music, name='music-retrieve'),
    path('musics/', MusicListView.as_view(), name='music-list'),
    path('history/add', HistoryCreateView.as_view(), name='history-create'),
    path('history/read', HistoryListView.as_view(), name='history-read'),
]
