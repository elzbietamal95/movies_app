from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from accounts.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View


class UserLoginView(View):
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return redirect('accounts:panel')

    def get(self, request):
        return render(request, 'accounts/login.html', {'form': LoginForm})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        #TO DO
        #else:
           # return self.form_invalid(form)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # user = form.get_user()
            if user is not None and user.is_active:
                login(request, user)
                return redirect('accounts:panel')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'accounts/logout.html')


def user_signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/registration_done.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required(login_url="/accounts/login/")
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
    user_to_delete = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('accounts:user-list')
    else:
        return render(request, 'accounts/user_delete.html', context={'user_to_delete': user_to_delete})