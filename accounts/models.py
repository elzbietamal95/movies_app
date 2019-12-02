from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #is_admin = models.BooleanField('admin status', default=False)
    USERNAME_FIELD = 'email'
    email = models.EmailField('email address', unique=True)
    REQUIRED_FIELDS = []
