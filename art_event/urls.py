from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib import admin

# from telegram_bot.views import webhook, telegram_bot
# from telegram_bot.telegram_bot import set_webhook, webhook
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required
from . import views

app_name = "art_event"  # добавьте это, если используете пространства имен


urlpatterns = [
    path("art_event/articles/", views.ArticleListView.as_view(), name="articles"),
    path("art_event/articles/add/", views.add_article, name="add_article"),
    path(
        "art_event/articles/<int:pk>/update/",
        views.ArticleUpdateView.as_view(),
        name="update_article",
    ),
    path("art_event/events/", views.events, name="events"),
    path("art_event/events/add/", views.EventCreateView.as_view(), name="add_event"),
    path(
        "art_event/events/<int:pk>/update/",
        views.EventUpdateView.as_view(),
        name="update_event",
    ),
    path(
        "art_event/events/<int:pk>/delete/",
        views.EventDeleteView.as_view(),
        name="delete_event",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
