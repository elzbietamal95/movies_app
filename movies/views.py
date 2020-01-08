from django.shortcuts import render
from .models import Movie
from django.views.generic import ListView, CreateView
from movies.forms import MovieCreateForm


class MovieList(ListView):
    context_object_name = 'movies'
    queryset = Movie.objects.all()
    model = Movie
    template_name = 'movies/movie_list.html'


class MovieCreate(CreateView):
    model = Movie
    form_class = MovieCreateForm
    template_name = 'movies/movie_add.html'
