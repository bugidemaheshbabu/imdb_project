from django.shortcuts import render
from imdb.models import *

# Create your views here.

def home(request) :
    movies_list = Movie.objects.all()
    context = {'movies_list' : movies_list}
    return render(request, 'imdb_home.html',context)

def movie(request, movie_id) :
    movie = Movie.objects.get(movie_id = movie_id)
    cast = Cast.objects.filter(movie = movie)
    return render(request, 'imdb_movie.html', {'movie' : movie,'cast' : cast})
        

def actor(request, actor_id) :
    actor = Actor.objects.get(actor_id = actor_id)
    cast = list(Cast.objects.filter(actor = actor))
    context = {
        'actor' : actor,
        'cast' : cast
     }
    return render(request, 'imdb_actor.html', context )

def director(request, name) :
    director = Director.objects.get(name = name)
    movies = list(Movie.objects.filter(director = director))
    context = {
        'director' : director,
        'movies' : movies
    }
    return render(request, 'imdb_director.html', context)

def analytics(request) :
    from imdb.utils import collections_by_genre,movie_collections_in_polar_data,movie_collections_as_per_year,movie_collections_in_single_bar,collection_of_actor

    data = movie_collections_in_single_bar()

    # collection_of_actor_data = collection_of_actor()
    # data.update(collection_of_actor_data)

    collections_by_genre_data = collections_by_genre()
    data.update(collections_by_genre_data)
    
    movie_collections_as_per_year_data = movie_collections_as_per_year()
    data.update(movie_collections_as_per_year_data)

    movie_collections_in_polar_data_data = movie_collections_in_polar_data()
    data.update(movie_collections_in_polar_data_data)

    return render(request, 'analytics.html', data)

