from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required
from . import views
from .views import my_view

app_name = "helpy"  # добавьте это, если используете пространства имен


urlpatterns = [
    path("helpy/help/", views.search_helpers, name="help"),
    path("helpy/helpmy/", views.HelpMyView.as_view(), name="helpmy"),
    path("helpy/set_language/", RedirectView.as_view(url="/"), name="set_language"),
    path("helpy/helpers/", views.HelperListView.as_view(), name="helper_list"),
    path("helpy/helpers/add/", views.helper_form, name="add_helper"),
    path(
        "helpy/helpers/<int:pk>/update/",
        views.HelperUpdateView.as_view(),
        name="update_helper_info",
    ),
    path(
        "helpy/helpers/<int:pk>/delete/",
        views.HelperDeleteView.as_view(),
        name="delete_helper",
    ),
    path("helpy/about/", views.about, name="about"),
    path("helpy/donate/", views.donate_view, name="donate"),
    path("helpy/success/", views.success, name="success"),
    path("helpy/menu/", views.my_view, name="my_menu"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
