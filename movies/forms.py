from django import forms
from movies.models import Movie, Actor, Role


class MovieCreateForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'year_of_production', 'image', 'short_description',)


class MovieEditForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'year_of_production', 'image', 'short_description')


class ActorCreateForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ('first_name', 'last_name', 'image')


class RoleCreateForm(forms.ModelForm):
    movie = forms.ModelChoiceField(queryset=Movie.objects.all(), widget=forms.Select)

    class Meta:
        model = Role
        fields = ('movie', 'role')


RoleFormSet = forms.inlineformset_factory(
    parent_model=Actor,
    model=Role,
    form=RoleCreateForm,
    extra=3,
    can_delete=False,

)


class ActorEditForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = '__all__'
