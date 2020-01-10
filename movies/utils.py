from django.utils.text import slugify


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
