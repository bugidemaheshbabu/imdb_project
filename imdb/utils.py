from imdb.models import *
from datetime import date


def populate_actors() :
    import json
    f_5000 = open("/home/rguktrkv/Desktop/complete_data/actors_5000.json","r")
    f = open("/home/rguktrkv/Downloads/100_movies/actors_100.json","r")
    actors_list = f.read()
    actor_json_list = json.loads(actors_list)
    for actor in actor_json_list:
        Actor.objects.create(
        actor_id = actor['actor_id'],
        name=actor['name'],
        gender = actor['gender']
    )
    
def populate_directors():
    import json
    f_5000 = open("/home/rguktrkv/Desktop/complete_data/directors_5000.json","r")
    f = open("/home/rguktrkv/Downloads/100_movies/directors_100.json","r")
    directors_list = f.read()
    directors_json_list = json.loads(directors_list) 
    for director in directors_json_list :
        Director.objects.create(
            name = director['name'],
            gender = director['gender']
        )   
    
import random
actors_role = ['Hero','villan','Heroine','Comedian','Child','Co-star']
def populate_movies():
    import json
    import uuid
    f_500 = open("/home/rguktrkv/Desktop/complete_data/movies_5000.json","r")
    f = open("/home/rguktrkv/Downloads/100_movies/movies_100.json","r")
    movies_list = f.read()
    movies_json_list = json.loads(movies_list) 
#    print(movies_json_list[:10])
    for movie in movies_json_list : 
        if movie['year_of_release'] == '' :
            movie['year_of_release'] = '0'
        if movie['budget'] == '' :
            movie['budget'] = '0'
        movie_obj = Movie.objects.create(movie_id = uuid.uuid4(),
            name = movie['name'],
            box_office_collection_in_crores = movie['box_office_collection_in_crores'],
            director = Director.objects.get(name = movie['director_name']),
            year_of_release = int(movie['year_of_release']),
            budget = int(movie['budget']),
            language  = movie['language'],
            average_rating = movie['average_rating']
        )
        for actor in movie['actors']:
            Cast.objects.create(
                    actor = Actor.objects.get(actor_id = actor['actor_id']),
                    movie = movie_obj,
                    role = random.choice(actors_role)
            )
        for genre in movie['genres'] :
            try :
                movie_obj.genres.add(Genre.objects.get(genre = genre))
            except Genre.DoesNotExist :
                movie_obj.genres.add(Genre.objects.create(genre = genre))

        

def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    
    for actor in actors_list:
        Actor.objects.create(actor_id = actor['actor_id'],name=actor['name'],date_of_birth = actor['date_of_birth'],gender = actor['gender'])
        
    for director in directors_list:        
        Director.objects.create(name=director)
        
    for movie in movies_list:
        Movie.objects.create(movie_id = movie['movie_id'],
            name = movie['name'],
            box_office_collection_in_crores = movie['box_office_collection_in_crores'],
            release_date = movie['release_date'],
            director = Director.objects.get(name = movie['director_name']),
            genre = movie['genre']
        )
        for actor in movie['actors']:
            Cast.objects.create(
                    actor = Actor.objects.get(actor_id = actor['actor_id']),
                    movie = Movie.objects.get(movie_id = movie['movie_id']),
                    role = actor['role'],
                    is_debut_movie = actor['is_debut_movie']
            )
    
    for movie_rate in movie_rating_list:
        Rating.objects.create(
            movie = Movie.objects.get(movie_id = movie_rate['movie_id']),
            rating_one_count = movie_rate['rating_one_count'],
            rating_two_count = movie_rate['rating_two_count'],
            rating_three_count = movie_rate['rating_three_count'],
            rating_four_count = movie_rate['rating_four_count'],
            rating_five_count = movie_rate['rating_five_count']
        )

    

def get_one_bar_plot_data():
    import json
    single_bar_chart_data = {
        "labels": ["Sun", "Mon", "Tu", "Wed", "Th", "Fri", "Sat"],
        "data": [40, 55, 75, 81, 56, 55, 40],
        "name": "Single Bar Chart",
        "borderColor": "rgba(0, 123, 255, 0.9)",
        "border_width": "0",
        "backgroundColor": "rgba(0, 123, 255, 0.5)"
    }
    return {
        'single_bar_chart_data_one': json.dumps(single_bar_chart_data),
        'single_bar_chart_data_one_title': 'Title'
    }

def movie_collections_in_single_bar() :
    import json
    from imdb.models import Movie
    movie_collections = Movie.objects.values_list('box_office_collection_in_crores', flat = True)[:5]
    movie_names = Movie.objects.values_list('name', flat = True)[:5]
    
    single_bar_chart_data = {
        "labels": list(movie_names),
        "datasets" : [
            {
                "data": list(movie_collections),
                "name": "Single Bar Chart",
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "border_width": "0",
                "backgroundColor": "rgba(0, 123, 255, 0.5)"        
            }    
        ]
        
    }
    return {
        'single_bar_chart_data_one': json.dumps(single_bar_chart_data),
        'single_bar_chart_data_one_title': 'Title'
    }

def collection_of_actor() :
    import json
    from imdb.models import Movie
    collections_list = execute_sql_query("select name,box_office_collection_in_crores  from imdb_movie WHERE movie_id IN(select movie_id from imdb_cast WHERE actor_id = 'actor_1') LIMIT 5;")
    collections = []
    movie_name =[]
    for item in collections_list :
        collections.append(item[1])
        movie_name.append(item[0])
    single_bar_chart_data = {
        "labels": list(movie_name),
        "datasets" : [
            {
                "data": list(collections),
                "name": "Single Bar Chart",
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "border_width": "0",
                "backgroundColor": "rgba(0, 123, 255, 0.5)"        
            }    
        ]
        
    }
    return {
        'single_bar_chart_data_one': json.dumps(single_bar_chart_data),
        'single_bar_chart_data_one_title': 'Actor Recent Collecions'
    }


def get_two_bar_plot_data():
    import json
    multi_bar_plot_data = {
        "labels": ["January", "February", "March", "April", "May", "June",
                   "July"],
        "datasets": [
            {
                "label": "My First dataset",
                "data": [65, 59, 80, 81, 56, 55, 40],
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "borderWidth": "0",
                "backgroundColor": "rgba(0, 123, 255, 0.5)",
                "fontFamily": "Poppins"
            },
            {
                "label": "My Second dataset",
                "data": [28, 48, 40, 19, 86, 27, 90],
                "borderColor": "rgba(0,0,0,0.09)",
                "borderWidth": "0",
                "backgroundColor": "rgba(0,0,0,0.07)",
                "fontFamily": "Poppins"
            }
        ]
    }

    return {
        'multi_bar_plot_data_one': json.dumps(multi_bar_plot_data),
        'multi_bar_plot_data_one_title': 'Title'
    }


def get_multi_line_plot_data():
    import json
    multi_line_plot_data = {
        "labels": ["2010", "2011", "2012", "2013", "2014", "2015", "2016"],
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "label": "Foods",
            "data": [0, 30, 10, 120, 50, 63, 10],
            "backgroundColor": 'transparent',
            "borderColor": 'rgba(220,53,69,0.75)',
            "borderWidth": 3,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(220,53,69,0.75)',
        }, {
            "label": "Electronics",
            "data": [0, 50, 40, 80, 40, 79, 120],
            "backgroundColor": 'transparent',
            "borderColor": 'rgba(40,167,69,0.75)',
            "borderWidth": 3,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(40,167,69,0.75)',
        }]
    }
    return {
        'multi_line_plot_data_one': json.dumps(multi_line_plot_data),
        'multi_line_plot_data_one_title': 'Title'
    }




def get_area_plot_data():
    import json
    area_plot_data = {
        "labels": ["2010", "2011", "2012", "2013", "2014", "2015", "2016"],
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "data": [0, 7, 3, 5, 2, 10, 7],
            "label": "Expense",
            "backgroundColor": 'rgba(0,103,255,.15)',
            "borderColor": 'rgba(0,103,255,0.5)',
            "borderWidth": 3.5,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(0,103,255,0.5)',
        }, ]
    }
    return {
        'area_plot_data_one': json.dumps(area_plot_data),
        'area_plot_data_one_title': 'Title'
    }

def movie_collections_as_per_year() :
    import json
    from imdb.models import Movie
    from imdb.utils import execute_sql_query
    collections_list = execute_sql_query('select SUM(box_office_collection_in_crores),year_of_release as year from imdb_movie GROUP BY year')
    collections = []
    collections_year =[]
    for item in collections_list :
        collections.append(item[0])
        collections_year.append(item[1])
    area_plot_data = {
        "labels": collections_year,
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "data": collections,
            "label": "Expense",
            "backgroundColor": 'rgba(0,103,255,.15)',
            "borderColor": 'rgba(0,103,255,0.5)',
            "borderWidth": 3.5,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(0,103,255,0.5)',
        }, ]
    }
    return {
        'area_plot_data_one': json.dumps(area_plot_data),
        'area_plot_data_one_title': 'Movie Collections'
    }

def no_of_movie_per_year():
    import json
    from imdb.models import Movie
    from imdb.utils import execute_sql_query
    collections_list = execute_sql_query('select year_of_release as year, COUNT(*) from (select * from (select * from imdb_movie  INNER JOIN imdb_cast  ON (imdb_movie.movie_id =imdb_cast.movie_id))where is_debut_movie = 1)group by year')
    collections = []
    collections_year =[]
    for item in collections_list :
        collections.append(item[0])
        collections_year.append(item[1])
    area_plot_data = {
        "labels": collections,
        "type": 'line',
        "defaultFontFamily": 'Poppins',
        "datasets": [{
            "data": collections_year,
            "label": "Expense",
            "backgroundColor": 'rgba(0,103,255,.15)',
            "borderColor": 'rgba(0,103,255,0.5)',
            "borderWidth": 3.5,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointBorderColor": 'transparent',
            "pointBackgroundColor": 'rgba(0,103,255,0.5)',
        }, ]
    }
    return {
        'area_plot_data_one': json.dumps(area_plot_data),
        'area_plot_data_one_title': 'Number of Movies releasing per year'
    }



def get_radar_chart_data():
    import json
    radar_chart_data = {
        "labels": [["Eating", "Dinner"], ["Drinking", "Water"], "Sleeping",
                   ["Designing", "Graphics"], "Coding", "Cycling", "Running"],
        "defaultFontFamily": 'Poppins',
        "datasets": [
            {
                "label": "My First dataset",
                "data": [65, 59, 66, 45, 56, 55, 40],
                "borderColor": "rgba(0, 123, 255, 0.6)",
                "borderWidth": "1",
                "backgroundColor": "rgba(0, 123, 255, 0.4)"
            },
            {
                "label": "My Second dataset",
                "data": [28, 12, 40, 19, 63, 27, 87],
                "borderColor": "rgba(0, 123, 255, 0.7",
                "borderWidth": "1",
                "backgroundColor": "rgba(0, 123, 255, 0.5)"
            }
        ]
    }
    return {
        'radar_chart_data_one': json.dumps(radar_chart_data),
        'radar_chart_data_one_title': 'Title'
    }


def get_doughnut_chart_data():
    import json
    doughnut_graph_data = {
        "datasets": [{
            "data": [45, 25, 20, 10],
            "backgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ],
            "hoverBackgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ]

        }],
        "labels": [
            "Green1",
            "Green2",
            "Green3",
            "Green4"
        ]
    }

    return {
        'doughnut_graph_data_one': json.dumps(doughnut_graph_data),
        'doughnut_graph_data_one_title': 'Title'
    }

def movie_collections_in_doughnut_chart() :
    import json
    from imdb.models import Movie
    movie_collections = Movie.objects.values_list('box_office_collection_in_crores', flat = True)
    movie_names = Movie.objects.values_list('name', flat = True)
    doughnut_graph_data = {
        "datasets": [{
            "data": list(movie_collections),
            "backgroundColor": [
                "rgbcde(136, 176, 75)",
                "rgba(80, 12, 100,0.7)",
                "rgba(70, 223, 55,0.5)",
                "rgba(0,0,0,0.07)"
            ],
            "hoverBackgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ]

        }],
        "labels": list(movie_names)
    }
    

    return {
        'doughnut_graph_data_one': json.dumps(doughnut_graph_data),
        'doughnut_graph_data_one_title': 'Title',
    }


def collections_by_genre() :
    import json
    from imdb.models import Movie
    collections_list = execute_sql_query("select SUM(box_office_collection_in_crores),genre_id from imdb_movie as mv inner join imdb_movie_genres as gn on (mv.movie_id = gn.movie_id) group by genre_id order by genre_id ASC LIMIT 5;")
    collections = []
    genre =[]
    for item in collections_list :
        collections.append(item[0])
        genre.append(item[1])
    doughnut_graph_data = {
        "datasets": [{
            "data": list(collections),
            "backgroundColor": [
                "rgbcde(136, 176, 75)",
                "rgba(80, 12, 100,0.7)",
                "rgba(70, 223, 55,0.5)",
                "rgba(0,0,0,0.07)"
            ],
            "hoverBackgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ]

        }],
        "labels": list(genre)
    }
    

    return {
        'doughnut_graph_data_one': json.dumps(doughnut_graph_data),
        'doughnut_graph_data_one_title': 'Collections by Genre',
    }


def get_multi_line_plot_with_area_data():
    import json
    multi_line_plot_with_area_data = {
        "labels": [
            "January", "February", "March", "April", "May", "June",
            "July"],
        "defaultFontFamily": "Poppins",
        "datasets": [
            {
                "label": "My First dataset",
                "borderColor": "rgba(0,0,0,.09)",
                "borderWidth": "1",
                "backgroundColor": "rgba(0,0,0,.07)",
                "data": [22, 44, 67, 43, 76, 45, 12]
            },
            {
                "label": "My Second dataset",
                "borderColor": "rgba(0, 123, 255, 0.9)",
                "borderWidth": "1",
                "backgroundColor": "rgba(0, 123, 255, 0.5)",
                "pointHighlightStroke": "rgba(26,179,148,1)",
                "data": [16, 32, 18, 26, 42, 33, 44]
            }
        ]
    }

    return {
        'multi_line_plot_with_area_data_one': json.dumps(
            multi_line_plot_with_area_data),
        'multi_line_plot_with_area_data_one_title': 'Title'
    }


def get_pie_chart_data():
    import json

    pie_chart_data = {
        "datasets": [{
            "data": [45, 25, 20, 10],
            "backgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ],
            "hoverBackgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0, 123, 255,0.5)",
                "rgba(0,0,0,0.07)"
            ]

        }],
        "labels": [
            "Green",
            "Green",
            "Green"
        ]
    }

    return {
        'pie_chart_data_one': json.dumps(
            pie_chart_data),
        'pie_chart_data_one_title': 'Title'
    }


def get_polar_chart_data():
    import json

    polar_chart_data = {
        "datasets": [{
            "data": [15, 18, 9, 6, 19],
            "backgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.8)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0,0,0,0.2)",
                "rgba(0, 123, 255,0.5)"
            ]

        }],
        "labels": [
            "Green1",
            "Green2",
            "Green3",
            "Green4",
            "Green5"
        ]
    }
    return {
        'polar_chart_data_one': json.dumps(
            polar_chart_data),
        'polar_chart_data_one_title': 'Title'
    }

def movie_collections_in_polar_data() :
    import json
    from imdb.models import Movie
    movie_collections = Movie.objects.values_list('box_office_collection_in_crores', flat = True)[:5]
    movie_names = Movie.objects.values_list('name', flat = True)[:5]
    
    polar_chart_data = {
        "datasets": [{
            "data": list(movie_collections),
            "backgroundColor": [
                "rgba(0, 123, 255,0.9)",
                "rgba(0, 123, 255,0.8)",
                "rgba(0, 123, 255,0.7)",
                "rgba(0,0,0,0.2)",
                "rgba(0, 123, 255,0.5)"
            ]

        }],
        "labels": list(movie_names)
    }
    return {
        'polar_chart_data_one': json.dumps(
            polar_chart_data),
        'polar_chart_data_one_title': 'Title'
    }


def execute_sql_query(sql_query):
    """
    Executes sql query and return data in the form of lists (
        This function is similar to what you have learnt earlier. Here we are
        using `cursor` from django instead of sqlite3 library
    )
    :param sql_query: a sql as string
    :return:
    """
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
    return rows
