from django import forms
from movies.models import Movie


class MovieCreateForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'slug', 'year_of_production', 'image', 'short_description', 'actors')
