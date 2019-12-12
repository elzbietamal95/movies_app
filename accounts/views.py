from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from accounts.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View


class UserAuthBaseView(View):
    template_name = None
    form_class = None

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        pass


class UserLoginView(UserAuthBaseView):
    template_name = 'accounts/login.html'
    success_url = 'accounts:panel'
    form_class = LoginForm
    # redirect_field_name = 'next'
    # TO DO: fix the parameter next!

    def form_valid(self, form):
        user = form.get_user()
        if user is not None and user.is_active:
            login(self.request, user)
            return redirect(self.success_url)


class UserRegistrationView(UserAuthBaseView):
    form_class = RegistrationForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'accounts/registration_done.html', {'form': form})


class UserLogoutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request):
        logout(request)
        return render(self.request, self.template_name)


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