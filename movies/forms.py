from django import forms
from movies.models import Movie, Actor


class MovieCreateForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'year_of_production', 'image', 'short_description',)


class MovieEditForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'year_of_production', 'image', 'short_description')
