from django import template
from django.urls import reverse


register = template.Library()
@register.simple_tag
def render_menu(request):
    menu_items = [
        {'title': 'Helpy', 'url': reverse('index')},
        {'title': 'Offer help', 'url': reverse('offer_help')},
        {'title': 'Articles', 'url': reverse('articles')},
        {'title': 'Events', 'url': reverse('events')},
        {'title': 'About', 'url': reverse('about')},
    ]

    def get_menu_html(current_view_name):
        menu_html = '<nav class="navbar navbar-expand-lg navbar-light bg-light">' \
                    '<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">' \
                    '<span class="navbar-toggler-icon"></span>' \
                    '</button>' \
                    '<div class="collapse navbar-collapse" id="navbarNav">' \
                    '<ul class="navbar-nav mr-auto">'
        for item in menu_items:
            menu_html += '<li class="nav-item {% if item.url == current_view_name %}active{% endif %}">' \
                         '<a class="nav-link" href="' + item['url'] + '">' + item['title'] + '</a>' \
                         '</li>'
        menu_html += '</ul></div></nav>'

        return menu_html

    current_view_name = request.resolver_match.view_name
    return get_menu_html(current_view_name)
