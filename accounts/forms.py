from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')