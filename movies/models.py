from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    actors = models.CharField(max_length=500)
    runtime = models.IntegerField()
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    # 加 

    def __str__(self):
        return self.title



class Collection(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name


# Create your models here.
