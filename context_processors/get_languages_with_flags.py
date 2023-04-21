from django.templatetags.static import static
from django.conf import settings


def get_languages_with_flags(languages):
    languages_with_flags = []
    for code, name in languages:
        language_with_flag = {
            'code': code,
            'name': name,
            'flag': static(f'flags/{code}.svg'),
        }
        languages_with_flags.append(language_with_flag)
    return languages_with_flags