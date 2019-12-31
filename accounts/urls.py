from django.urls import path
from accounts import views
from accounts.views import UserLogoutView, UserLoginView, UserRegistrationView

app_name = 'accounts'

urlpatterns = [
    path('', views.user_panel, name='panel'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='signup'),
    path('user-list/', views.user_list_view, name='user-list'),
    path('<username>/', views.user_profile, name='profile'),
    path('<username>/edit/', views.user_edit_view, name='user-edit'),
    path('<username>/delete/', views.user_delete_view, name='user-delete')
]