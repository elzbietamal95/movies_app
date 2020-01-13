from django.urls import path, include
from accounts import views
from accounts.views import UserLogoutView, UserLoginView, UserRegistrationView, UserList

app_name = 'accounts'

urlpatterns = [
    path('', views.user_panel, name='panel'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='signup'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<username>/', views.user_profile, name='profile'),
    path('users/<username>/edit/', views.user_edit_view, name='user-edit'),
    path('users/<username>/delete/', views.user_delete_view, name='user-delete'),
    # API
    path('api/', include('accounts.api.urls')),
]