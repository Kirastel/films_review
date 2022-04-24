from django.urls import reverse
from urllib.parse import urlencode
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Replaces value of url parameter (such as page=value in pagination).
    """
    query = context.get('request').GET.copy()
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag(takes_context=True)
def url_next(context, **kwargs):
    cur_path = context.get('request').path

    if cur_path not in [reverse('user:login'), reverse('user:register'), reverse('films_review:my_reviews')]:
        return '?' + urlencode(kwargs)
    else:
        return ''


@register.simple_tag(takes_context=True)
def get_page_range(context, on_each_side=2, on_ends=1):
    cur_page = context.get('page_obj').number
    page_range = context.get('paginator').get_elided_page_range(cur_page, on_each_side=on_each_side, on_ends=on_ends)

    return page_range
