from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractUser,
                                        AbstractBaseUser,
                                        _user_has_module_perms,
                                        Permission,
                                        _user_get_all_permissions,
                                        _user_has_perm)


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        extra_fields.setdefault('is_admin', True)
        return self._create_user(email, username, password, **extra_fields)


class CustomPermissions(models.Model):
    is_admin = models.BooleanField(
        verbose_name='admin status',
        default=False,
        help_text='Designates that this user has all permissions without '
                  'explicitly assigning them.',
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_admin:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_admin:
            return True

        return _user_has_module_perms(self, app_label)


class User(AbstractBaseUser, CustomPermissions):
    """
    A base class implementing a fully featured User model with
    admin-compliant permissions.

    Email address, username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        help_text='Required.',
        error_messages={
            'unique': "A user with that email address already exists.",
        },
    )
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(verbose_name='first name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=150, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def is_staff(self):
        return self.is_admin
