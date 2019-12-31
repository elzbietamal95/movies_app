from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.http import HttpResponseRedirect
from accounts.models import User
from django.contrib.auth import login, logout, get_user_model
from accounts.forms import LoginForm, CustomUserCreationForm, CustomUserChangeForm, UserEditForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View
from movies_app import settings

# User = get_user_model()
login_redirect_url = settings.LOGIN_REDIRECT_URL


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
    # TO DO: add method form_invalid (parameter 'next' doesn't always work!)
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_field_name = 'next'

    def get_success_url(self):
        url = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        return url or resolve_url(login_redirect_url)

    def form_valid(self, form):
        user = form.get_user()
        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())


class UserRegistrationView(UserAuthBaseView):
    form_class = CustomUserCreationForm
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


@login_required(login_url="/accounts/login/")
def user_profile(request, username):
    profile_of_user = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', context={'profile_of_user': profile_of_user})


def is_admin(user):
    return user.is_admin


@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def user_list_view(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'accounts/user_list.html', context={'users': users})


@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def user_edit_view(request, username):
    user_to_edit = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user_edit_form = UserEditForm(data=request.POST, instance=user_to_edit)
        if user_edit_form.is_valid():
            user_edit_form.save()
            messages.success(request, 'User was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_edit_form = UserEditForm(instance=user_to_edit)
    return render(request, 'accounts/user_edit.html', context={'user_edit_form': user_edit_form,
                                                               'user_to_edit': user_to_edit})


@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def user_delete_view(request, username):
    user_to_delete = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('accounts:user-list')
    else:
        return render(request, 'accounts/user_delete.html', context={'user_to_delete': user_to_delete})