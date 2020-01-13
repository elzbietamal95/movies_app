from django.urls import path
from movies.views import MovieList, MovieCreate

app_name = 'movies'

urlpatterns = [
    path('', MovieList.as_view(), name='movie-list'),
    path('movie-add/', MovieCreate.as_view(), name='movie-add'),
]