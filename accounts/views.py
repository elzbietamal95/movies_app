from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from accounts.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            user = authenticate(email=clean['email'], password=clean['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authentication succeeded.')
                else:
                    return HttpResponse('Account is locked.')
            else:
                return HttpResponse('Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html')

def user_signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('account')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def user_panel(request):
    return render(request, 'accounts/panel.html', {'section': 'panel'})