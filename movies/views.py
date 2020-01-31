from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from movies.utils import get_unique_slug
from .models import Movie, Actor
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from movies.forms import MovieCreateForm, MovieEditForm, ActorCreateForm, ActorEditForm


class MovieList(ListView):
    context_object_name = 'movies'
    model = Movie
    template_name = 'movies/movie_list_main.html'


class MovieCreate(CreateView):
    model = Movie
    form_class = MovieCreateForm
    template_name = 'movies/movie_add.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        movie = form.save()
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


class MovieEdit(UpdateView):
    model = Movie
    template_name = 'movies/movie_edit.html'
    form_class = MovieEditForm
    context_object_name = 'movie'
    success_url = 'movies:movie-detail'

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.slug = get_unique_slug(movie.pk, movie.title, Movie.objects)
        movie.save()
        messages.success(self.request, 'The movie "' + movie.title + '" was updated successfully!')
        return redirect(self.get_success_url())


class ActorList(ListView):
    context_object_name = 'actors'
    model = Actor
    template_name = 'movies/actor_list_main.html'


class ActorCreate(CreateView):
    model = Actor
    form_class = ActorCreateForm
    template_name = 'movies/actor_add.html'

    def form_valid(self, form):
        actor = form.save()
        messages.success(self.request, 'The actor "' + str(actor) + '" was added successfully!')
        return redirect('movies:actor-list')


class ActorDetail(DetailView):
    model = Actor


class ActorEdit(UpdateView):
    model = Actor
    template_name = 'movies/actor_edit.html'
    form_class = ActorEditForm
    context_object_name = 'actor'
    success_url = 'movies:actor-detail'

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        actor = form.save()
        messages.success(self.request, 'The actor "' + str(actor) + '" was updated successfully!')
        return redirect(self.get_success_url())
