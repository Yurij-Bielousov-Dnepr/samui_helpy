from django import template
from django_countries import countries
from django.conf.locale import LANG_INFO

register = template.Library()

LANGUAGE_TO_COUNTRY_MAP = {
    'uk': 'UA',
    'th': 'TH',
    'en': 'US',
    'fr': 'FR',
    'it': 'IT',
    'de': 'DE',
    'ru': 'RU',
}


def country_flag(value):
    country = countries.by_code( value )
    if country:
        return country.flag
    return ''


register.filter( 'country_flag', country_flag )


def language_to_country(value):
    return LANGUAGE_TO_COUNTRY_MAP.get( value, '' )


register.filter( 'language_to_country', language_to_country )
