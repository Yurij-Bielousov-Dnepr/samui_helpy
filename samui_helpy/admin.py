from django.contrib import admin
from reviews.models import Review, Re_view
from offer.models import Helper
from helpy.models import Tag_help, HelpRequest, HelpRequestLanguage
from art_event.models import Article, Event
from accounts.models import (
    Sponsor,
    Stats,
    Language,
    SupportLevel,
    Region,
    Level,
    Favorites,
)

# admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Event)
admin.site.register(Helper)
admin.site.register(Review)
admin.site.register(Tag_help)
admin.site.register(Sponsor)
admin.site.register(Re_view)
admin.site.register(Stats)


@admin.register(Language, SupportLevel, HelpRequest, Region, HelpRequestLanguage, Level)
class HiddenAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
