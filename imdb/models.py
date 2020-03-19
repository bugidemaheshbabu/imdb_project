from django.db import models
from datetime import date

# Create your models here.

class Director(models.Model):
    name = models.CharField(max_length = 200,primary_key = True)
    gender = models.CharField(max_length = 100)

class Actor(models.Model):
    actor_id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length = 100)
    gender = models.CharField(max_length = 100)

class Genre(models.Model) :
    genre = models.CharField(max_length = 100, primary_key=True)

class Movie(models.Model):
    name = models.CharField(max_length=100)
    movie_id = models.CharField(max_length=100,primary_key=True)
    year_of_release = models.IntegerField()
    box_office_collection_in_crores = models.FloatField()
    director = models.ForeignKey(Director,on_delete = models.CASCADE,)
    actors = models.ManyToManyField(Actor,through='Cast')
    budget = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    language = models.CharField(max_length = 100)
    average_rating = models.FloatField()

    # @property
    # def movie_avg_rating(self):
    #     try:
    #         one = self.rating.rating_one_count
    #         two = self.rating.rating_two_count
    #         three = self.rating.rating_three_count
    #         four = self.rating.rating_four_count
    #         five = self.rating.rating_five_count
    #         total_ratings = one + two*2 + three*3 + four*4 + five*5
    #         avg_rating = total_ratings / (one+two+three+four+five)
    #         return round(avg_rating,1)
    #     except ZeroDivisionError:
    #         return 0
    #     except Rating.DoesNotExist :
    #         return 0

class Cast(models.Model):
    actor = models.ForeignKey(Actor,on_delete = models.CASCADE,)
    movie = models.ForeignKey(Movie,on_delete = models.CASCADE,)
    role = models.CharField(max_length = 50, null = True)
    
# class Rating(models.Model):
#     movie = models.OneToOneField(Movie,on_delete=models.CASCADE,)
#     rating_one_count = models.IntegerField(default = 0)
#     rating_two_count = models.IntegerField(default = 0)
#     rating_three_count = models.IntegerField(default = 0)
#     rating_four_count = models.IntegerField(default = 0)
#     rating_five_count = models.IntegerField(default = 0)

    
        


