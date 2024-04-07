from django import template

register = template.Library()


@register.filter
def pluralize_likes(count):
    return 'Star' if count <= 1 else 'Stars'


