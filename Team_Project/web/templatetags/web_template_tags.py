from django import template
from web.models import Category

register = template.Library()


@register.inclusion_tag('web/categories.html')
def get_category_list():
    return {'categories': Category.objects.filter(tag__game_id__lt=2)}