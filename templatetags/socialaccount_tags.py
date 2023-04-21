from django import template
from allauth.socialaccount.templatetags.socialaccount import get_providers

register = template.Library()


@register.inclusion_tag('allauth/socialaccount/snippets/provider_list.html', takes_context=True)
def provider_list(context):
    """
    This tag is for rendering social djangoProject providers list
    """
    request = context.get('request')
    providers = get_providers(request)
    return {'providers': providers}
