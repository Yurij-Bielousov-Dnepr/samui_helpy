from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def get_menu_items(context):
    current_url = context['request'].path
    menu_items = [
        {'title': 'Helpy', 'url': reverse('index')},
        {'title': 'Offer help', 'url': reverse('offer_help')},
        {'title': 'Articles', 'url': reverse('articles')},
        {'title': 'Events', 'url': reverse('events')},
        {'title': 'About', 'url': reverse('about')},
    ]
    menu = []
    for item in menu_items:
        active = False
        if current_url == item['url']:
            active = True
        menu.append({'title': item['title'], 'url': item['url'], 'active': active})
    return menu
