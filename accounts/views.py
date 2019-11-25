from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            user = authenticate(username=clean['username'], password=clean['password'])
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

