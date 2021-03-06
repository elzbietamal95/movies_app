from django.urls import path
from movies.views import MovieList, MovieCreate, MovieDetail, MovieDelete, MovieEdit, ActorList, ActorCreate, \
    ActorDetail, ActorEdit, ActorDelete, DirectorList, DirectorDetail, DirectorCreate, DirectorDelete, DirectorEdit

app_name = 'movies'

urlpatterns = [
    path('', MovieList.as_view(), name='movie-list'),
    path('movie/movie-add/', MovieCreate.as_view(), name='movie-add'),
    path('movie/<slug:slug>/', MovieDetail.as_view(), name='movie-detail'),
    path('movie/<slug:slug>/#movie-delete-modal', MovieDelete.as_view(), name='movie-delete'),
    path('movie/<slug:slug>/edit', MovieEdit.as_view(), name='movie-edit'),
    path('actors/', ActorList.as_view(), name='actor-list'),
    path('actors/actor-add/', ActorCreate.as_view(), name='actor-add'),
    path('actors/<int:pk>/', ActorDetail.as_view(), name='actor-detail'),
    path('actors/<int:pk>/edit/', ActorEdit.as_view(), name='actor-edit'),
    path('actors/<int:pk>/#actor-delete-modal', ActorDelete.as_view(), name='actor-delete'),
    path('directors/', DirectorList.as_view(), name='director-list'),
    path('directors/<int:pk>/', DirectorDetail.as_view(), name='director-detail'),
    path('directors/director-add/', DirectorCreate.as_view(), name='director-add'),
    path('directors/<int:pk>/#director-delete-modal', DirectorDelete.as_view(), name='director-delete'),
    path('directors/<int:pk>/edit/', DirectorEdit.as_view(), name='director-edit'),
]