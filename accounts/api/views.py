import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User


def is_admin(user):
    return user.is_admin


@require_http_methods(['PUT'])
@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
# @csrf_exempt # only for test
def edit_user(request, username):
    user_to_edit = get_object_or_404(User, username=username)


@require_http_methods(['DELETE'])
@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def delete_user(request, username):
    user_to_delete = get_object_or_404(User, username=username)
    user_to_delete.delete()
    return JsonResponse({}, status=204)