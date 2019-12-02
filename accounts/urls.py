from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.user_panel, name='panel'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_signup, name='signup'),
    path('user-list/', views.user_list_view, name='user-list'),
    path('<username>/', views.user_edit_view, name='user-edit'),
    path('<username>/delete/', views.user_delete_view, name='user-delete')
]