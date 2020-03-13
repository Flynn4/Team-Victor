import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from web.models import Category

register = template.Library()


@register.inclusion_tag('web/categories.html')
def get_category_list():
    return {'categories': Category.objects.all()}


@stringfilter
def spacify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(re.sub('\s', '_', esc(value)))
spacify.needs_autoescape = True
register.filter(spacify)