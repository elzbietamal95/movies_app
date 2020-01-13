from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from movies.utils import get_unique_slug

User = get_user_model()


class Movie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, max_length=200, unique=True)
    year_of_production = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Use the following format < YYYY >.",
    )
    image = models.ImageField(upload_to='images/', blank=True)
    short_description = models.TextField(blank=True, max_length=1000, verbose_name='Description')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self.pk, self.title, Movie.objects)
        super(Movie, self).save(*args, **kwargs)

    def has_image(self):
        if self.image:
            return True
        else:
            return False
