from django.urls import path
from movies.views import MovieList

app_name = 'movies'

urlpatterns = [
    path('', MovieList.as_view(), name='movie-list'),
]