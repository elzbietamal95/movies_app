from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.functions import datetime


def get_unique_slug(pk, title, objects):
    slug = slugify(title)
    unique_slug = slug
    counter = 1
    while objects.filter(slug=unique_slug).exists():
        if objects.filter(slug=unique_slug).values('pk')[0]['pk'] == pk:
            break
        unique_slug = '{}-{}'.format(slug, counter)
        counter += 1
    return unique_slug


def year_validator(value):
    if value < 1850 or value > datetime.datetime.now().year + 5:
        raise ValidationError("%(value)s is not a correct year!", params={'value': value},)
