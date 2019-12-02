from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from accounts.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test

User = get_user_model()

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            user = authenticate(email=clean['email'], password=clean['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'accounts/panel.html', {'form': form})
                else:
                    print('Account is locked.')
            else:
                print('Invalid credentials.')
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
            return render(request, 'accounts/registration_done.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def user_panel(request):
    return render(request, 'accounts/panel.html')

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def user_list_view(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'accounts/user_list.html', context={'users': users})

def user_edit_view(request, username):
    return render(request, 'base.html')

def user_delete_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        return redirect('user-list')
    else:
        return render(request, 'accounts/user_delete.html', context={'user': user})