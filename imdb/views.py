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
    from .utils import no_of_movie_per_year,get_multi_line_plot_data,collections_by_genre,collection_of_actor,get_one_bar_plot_data,movie_collections_as_per_year,get_area_plot_data,get_radar_chart_data,movie_collections_in_polar_data,movie_collections_in_doughnut_chart,movie_collections_in_single_bar,get_area_plot_data
    
    """
    polar_data = movie_collections_in_polar_data()
    bar_data = movie_collections_in_single_bar()
    doughnut_data = movie_collections_in_doughnut_chart()
    area_data = get_area_plot_data()
    
    temp = get_radar_chart_data()
    temp.update(polar_data)
    temp.update(bar_data)
    temp.update(doughnut_data)
    temp.update(area_data)
    temp.update(collections_data)
    """
    
    temp = collection_of_actor()

    collections_data = movie_collections_as_per_year()
    temp.update(collections_data)
    
    collections_by_genre_data = collections_by_genre()
    temp.update(collections_by_genre_data)
    
    per_year = no_of_movie_per_year()
    temp.update(per_year)
    
    print(temp)
    return render(request, 'analytics.html', context = temp)