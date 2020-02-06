from django.contrib import admin
from .models import Actor, Role, Movie, Director


class RoleInLine(admin.TabularInline):
    model = Role
    extra = 3


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'year_of_production', 'image', 'added_by']
    list_filter = ['year_of_production']
    inlines = [RoleInLine]


class ActorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'image', 'added_by']
    inlines = [RoleInLine]


admin.site.register(Role)
admin.site.register(Director)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)
