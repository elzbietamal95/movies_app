from django.shortcuts import render
from .models import Movie
from django.views.generic import ListView


class MovieList(ListView):
    context_object_name = 'movies'
    queryset = Movie.objects.all()
    model = Movie
    template_name = 'movies/movie_list.html'
