from django.urls import path
from . import views

app_name = 'SNS'

urlpatterns = [
    path('api/', views.api_test, name='api_test'),
    path('home/', views.home, name='home'), 
    path('search/', views.search, name='search'),
    path('search/song/<slug:track_id>', views.song, name='song'),
    path('search/album/<slug:album_id>', views.album, name='album'),
    path('search/artist/<slug:artist_id>', views.artist, name='artist'),
    path('post/', views.post, name='post'),
    path('post/good', views.postGood, name='postgood'),
    path('post/delete', views.postDelete, name='postdelete'),
    path('spotify', views.spotify, name='spotify'),
    path('spotify/callback', views.spotify_callback, name='spotify_callback'),
    path('profile/<slug:username>', views.profile, name='profile'),
    path('check/username/', views.username_check, name='username_check'),
    path('search/song/', views.search_song, name='search_song'),
    path('signup/', views.AccountRegistration.as_view(), name='signup'), 
    path('signin/', views.Signin, name='signin'), 
    path('signout/', views.Signout, name='signout'),
    path('csrf_token/', views.csrf_token, name='csrf_token'),
]
