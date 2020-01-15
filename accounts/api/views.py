import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email

from accounts.models import User


def is_email_valid(email):
    try:
        validate_email(email)
    except validate_email.ValidationError:
        return False
    return True


def is_admin(user):
    return getattr(user, 'is_admin', False)


@require_http_methods(['PUT'])
def edit_user(request, username):
    if not is_admin(request.user):
        return JsonResponse({}, status=403)

    user = get_object_or_404(User, username=username)

    try:
        data = dict(json.loads(request.body))
    except (json.decoder.JSONDecodeError, TypeError):
        return JsonResponse({'non_field_errors': ['Body of the request must be a map in JSON format.']})

    errors = {}

    if 'username' not in data or not isinstance(data['username'], str) or not data['username']:
        errors['username'] = ['Username is required.']
    elif User.objects.filter(username=data['username']).exclude(pk=user.pk).exists():
        errors['username'] = ['A user with that username already exists.']

    if 'email' not in data:
        errors['email'] = ['Email address is required.']
    elif not is_email_valid(data['email']):
        errors['email'] = ['Enter a valid email address.']
    elif User.objects.filter(email=data['email']).exclude(pk=user.pk).exists():
        errors['email'] = ['A user with that email address already exists.']

    if 'first_name' in data and not isinstance(data['first_name'], str):
        errors['first_name'] = ['First name must be a string.']

    if 'last_name' in data and not isinstance(data['last_name'], str):
        errors['last_name'] = ['Last name must be a string.']

    if 'is_active' in data and not isinstance(data['is_active'], bool):
        errors['is_active'] = ['If user is active enter True, otherwise enter False.']

    if 'is_admin' in data and not isinstance(data['is_admin'], bool):
        errors['is_admin'] = ['If user is admin enter True, otherwise enter False.']

    if errors:
        return JsonResponse(errors, status=400)
    else:
        user.username = data['username']
        user.email = data['email']
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.is_active = data.get('is_active', user.is_active)
        user.is_admin = data.get('is_admin', user.is_admin)
        user.save()
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_admin': user.is_admin,
        }
        return JsonResponse(data, status=200)


@require_http_methods(['DELETE'])
@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def delete_user(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return JsonResponse({}, status=204)
