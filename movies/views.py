from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Movie
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import BaseDeleteView, DeleteView
from movies.forms import MovieCreateForm


class MovieList(ListView):
    context_object_name = 'movies'
    model = Movie
    template_name = 'movies/movie_list_main.html'


class MovieCreate(CreateView):
    model = Movie
    form_class = MovieCreateForm
    template_name = 'movies/movie_add.html'

    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.added_by = self.request.user
        form.instance.added_by = self.request.user
        movie.save()
        messages.success(self.request, 'The movie "' + movie.title + '" was added successfully!')
        return redirect('movies:movie-list')


class MovieDetail(DetailView):
    model = Movie


class MovieDelete(DeleteView):
    context_object_name = 'movie'
    model = Movie
    success_url = reverse_lazy('movies:movie-list')
    template_name = 'movies/movie_detail.html'

    def delete(self, request, *args, **kwargs):
        movie = self.get_object()
        messages.success(self.request, 'The movie "' + movie.title + '" was deleted successfully.')
        return super(MovieDelete, self).delete(request, *args, **kwargs)
