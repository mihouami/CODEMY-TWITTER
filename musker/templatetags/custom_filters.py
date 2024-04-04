from django import template

register = template.Library()


@register.filter
def pluralize_likes(count):
    return 'Star' if int(count) <= 1 else 'Stars'

