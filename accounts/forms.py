from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import User


class LoginForm(AuthenticationForm):
    pass


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email address', max_length=255, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')