from django import template
from allauth.utils import get_user_model

register = template.Library()


@register.filter
def is_authenticated(user):
    """
    This filter checks if user is authenticated and email address
    has been verified
    """
    if user.is_authenticated:
        from allauth.account.models import EmailAddress
        verified = EmailAddress.objects.filter(user=user, verified=True).exists()
        return verified
    return False


@register.inclusion_tag( 'accounts/snippets/login_form.html' )
def login_form(request, form=None):
    """
    This tag is for rendering login form template
    """
    return {'request': request, 'form': form}


@register.filter
def has_social_account(user):
    """
    This filter checks if user has any linked social djangoProject
    """
    if not user.is_authenticated:
        return False
    from allauth.socialaccount.models import SocialAccount
    has_social_account = SocialAccount.objects.filter(user=user).exists()
    return has_social_account


@register.inclusion_tag('account/snippets/provider_list.html', takes_context=True)
def provider_list(context):
    """
    This tag is for rendering social djangoProject providers list
    """
    from allauth.socialaccount.templatetags.socialaccount import get_providers
    request = context.get('request')
    providers = get_providers(request)
    return {'providers': providers}
