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

from ricommender_backend.authentication.views import UserLoginView
from ricommender_backend.authentication.views import UserRegisterView
from ricommender_backend.musicstreamer.views import MusicListView
from ricommender_backend.musicstreamer.views import MusicRetriever

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login/<slug:username>', UserLoginView.as_view(), name='user-login'),
    path('user/register', UserRegisterView.as_view(), name='user-register'),
    path('music/<music_id>', MusicRetriever.get_music, name='music-retrieve'),
    path('musics/', MusicListView.as_view(), name='music-list')
]