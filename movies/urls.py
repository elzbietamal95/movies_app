from django.urls import path
from movies.views import MovieList, MovieCreate, MovieDetail, MovieDelete, MovieEdit, ActorList, ActorCreate

app_name = 'movies'

urlpatterns = [
    path('', MovieList.as_view(), name='movie-list'),
    path('movie/movie-add/', MovieCreate.as_view(), name='movie-add'),
    path('movie/<slug:slug>/', MovieDetail.as_view(), name='movie-detail'),
    path('movie/<slug:slug>/#movie-delete-modal', MovieDelete.as_view(), name='movie-delete'),
    path('movie/<slug:slug>/edit', MovieEdit.as_view(), name='movie-edit'),
    path('actors/', ActorList.as_view(), name='actor-list'),
    path('actors/actor-add/', ActorCreate.as_view(), name='actor-add'),
]