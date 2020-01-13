from django.shortcuts import render, redirect
from django.contrib import messages
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

    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.added_by = self.request.user
        form.instance.added_by = self.request.user
        movie.save()
        messages.success(self.request, 'The movie ' + movie.title + ' was added successfully!')
        return redirect('movies:movie-list')
