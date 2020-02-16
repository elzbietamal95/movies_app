from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from movies.utils import get_unique_slug
from .models import Movie, Actor, Director
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from movies.forms import MovieForm, ActorForm, RoleFormSet


class MovieList(ListView):
    context_object_name = 'movies'
    model = Movie
    template_name = 'movies/movie_list_main.html'


class MovieCreate(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_add.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        if not (request.user.is_authenticated and request.user.is_admin or request.user == movie.added_by):
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        movie = self.get_object()
        messages.success(self.request, 'The movie "' + movie.title + '" was deleted successfully.')
        return super(MovieDelete, self).delete(request, *args, **kwargs)


class MovieEdit(UpdateView):
    model = Movie
    template_name = 'movies/movie_edit.html'
    form_class = MovieForm
    context_object_name = 'movie'
    success_url = 'movies:movie-detail'

    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        if not (request.user.is_authenticated and request.user.is_admin or request.user == movie.added_by):
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)

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
    form_class = ActorForm
    template_name = 'movies/actor_add.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        formset = RoleFormSet(self.request.POST)
        form = self.get_form()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form.instance.added_by = self.request.user
        actor = form.save()
        formset.instance = actor
        formset.save()
        messages.success(self.request, 'The actor "' + str(actor) + '" was added successfully!')
        return redirect('movies:actor-list')

    def form_invalid(self, form, formset):
        messages.error(self.request, 'Please correct the errors below.')
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['role_formset'] = RoleFormSet(self.request.POST)
        else:
            context['role_formset'] = RoleFormSet()
        return context


class ActorDetail(DetailView):
    model = Actor


class ActorEdit(UpdateView):
    model = Actor
    template_name = 'movies/actor_edit.html'
    form_class = ActorForm
    context_object_name = 'actor'
    success_url = 'movies:actor-detail'

    def get(self, request, *args, **kwargs):
        actor = self.get_object()
        if not (request.user.is_authenticated and request.user.is_admin or request.user == actor.added_by):
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ActorEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['role_formset'] = RoleFormSet(self.request.POST, instance=self.object)
            context['role_formset'].full_clean()
        else:
            context['role_formset'] = RoleFormSet(instance=self.object)
        return context

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['role_formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            actor = form.save(commit=False)
            messages.success(self.request, 'The actor "' + str(actor) + '" was updated successfully!')
            return response
        else:
            messages.error(self.request, 'Please correct the errors below.')
            return super().form_invalid(form)


class ActorDelete(DeleteView):
    context_object_name = 'actor'
    model = Actor
    success_url = reverse_lazy('movies:actor-list')
    template_name = 'movies/actor_detail.html'

    def get(self, request, *args, **kwargs):
        actor = self.get_object()
        if not (request.user.is_authenticated and request.user.is_admin or request.user == actor.added_by):
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        actor = self.get_object()
        messages.success(self.request, 'The actor "' + str(actor) + '" was deleted successfully.')
        return super(ActorDelete, self).delete(request, *args, **kwargs)


class DirectorList(ListView):
    context_object_name = 'directors'
    model = Director
    template_name = 'movies/director_list_main.html'