from django.contrib import admin
from .models import Actor, Role, Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'year_of_production', 'image', 'added_by']
    list_filter = ['year_of_production']


admin.site.register(Actor)
admin.site.register(Role)
admin.site.register(Movie, MovieAdmin)
