from django.contrib import admin
from .models import Actor, Role, Movie


class RoleInLine(admin.TabularInline):
    model = Role
    extra = 3


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'year_of_production', 'image', 'added_by']
    list_filter = ['year_of_production']
    inlines = [RoleInLine]


admin.site.register(Actor)
admin.site.register(Movie, MovieAdmin)
