from django.conf import settings
from . import get_languages_with_flags

def languages_with_flags(request):
    return {'languages_with_flags': get_languages_with_flags(settings.LANGUAGES)}
