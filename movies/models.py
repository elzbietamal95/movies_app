from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth import get_user_model
from star_ratings.models import Rating

from movies.utils import get_unique_slug, year_validator

User = get_user_model()


class Actor(models.Model):
    first_name = models.CharField(verbose_name='first name', max_length=50, help_text='Required.')
    last_name = models.CharField(verbose_name='last name', max_length=150, help_text='Required.')
    date_of_birth = models.DateField(blank=True, null=True, help_text='YYYY-MM-DD')
    place_of_birth = models.CharField(blank=True, max_length=200, null=True)
    height = models.PositiveIntegerField(blank=True, null=True, default=None, help_text='cm')
    image = models.ImageField(upload_to='images/actors', blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actors_created', blank=True, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'actor'
        verbose_name_plural = 'actors'
        ordering = ('last_name',)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_image(self):
        if self.image:
            return True
        return False


class Director(models.Model):
    first_name = models.CharField(verbose_name='first name', max_length=50, help_text='Required.')
    last_name = models.CharField(verbose_name='last name', max_length=150, help_text='Required.')
    date_of_birth = models.DateField(blank=True, null=True, help_text='YYYY-MM-DD')
    place_of_birth = models.CharField(blank=True, max_length=200, null=True)
    image = models.ImageField(upload_to='images/directors', blank=True)
    date_of_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='directors_created', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_image(self):
        if self.image:
            return True
        return False


class Movie(models.Model):
    title = models.CharField(max_length=200, help_text='Required.')
    slug = models.SlugField(blank=True, max_length=200, unique=True)
    year_of_production = models.PositiveIntegerField(
        validators=[year_validator],
        help_text="Required. Use the following format YYYY.",
    )
    image = models.ImageField(upload_to='images/movies', blank=True)
    short_description = models.TextField(blank=True, max_length=1000, verbose_name='Description')
    date_of_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies_created')
    actors = models.ManyToManyField(Actor, blank=True, through='Role', related_name='movies')
    directors = models.ManyToManyField(Director, blank=True, related_name='movies')
    rating = GenericRelation(Rating, related_query_name='movie')

    class Meta:
        verbose_name = 'movie'
        verbose_name_plural = 'movies'
        unique_together = ['title', 'year_of_production']
        ordering = ['title']

    objects = models.Manager()

    def __str__(self):
        return f"{self.title} ({self.year_of_production})"

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self.pk, self.title, Movie.objects)
        super(Movie, self).save(*args, **kwargs)

    def has_image(self):
        if self.image:
            return True
        return False


class Role(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='role')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.role

    class Meta:
        unique_together = ['movie', 'role']
