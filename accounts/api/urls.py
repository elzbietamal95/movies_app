from django.urls import path

from .views import edit_user, delete_user

app_name = 'api'

urlpatterns = [
    path('<username>/edit/', edit_user, name='edit-user'),
    path('<username>/delete/', delete_user, name='delete-user'),
]