from django.urls import path
from movies.views import MovieList, MovieCreate, MovieDetail

app_name = 'movies'

urlpatterns = [
    path('', MovieList.as_view(), name='movie-list'),
    path('movie/movie-add/', MovieCreate.as_view(), name='movie-add'),
    path('movie/<slug:slug>/', MovieDetail.as_view(), name='movie-detail'),
]