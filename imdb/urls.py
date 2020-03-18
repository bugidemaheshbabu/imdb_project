from django.urls import path
from . import views
from imdb.models import *

urlpatterns = [
    path('', views.home, name='homepage'),
    path('movie/<str:movie_id>/', views.movie, name='moviepage'),
    path('actor/<str:actor_id>/', views.actor, name='actorpage'),
    path('director/<str:name>/', views.director, name='directorpage'),
    path('analytics/', views.analytics, name='analyticspage'),
]

