from django.urls import path, include
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


app_name = "helpy"  # добавьте это, если используете пространства имен


urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/account_inactive/", views.account_inactive, name="account_inactive"),
    path("accounts/email/", views.email, name="email"),
    path("accounts/email_confirm/", views.email_confirm, name="email_confirm"),
    path("accounts/login/", views.login, name="account_login"),
    path("accounts/logout/", views.logout, name="account_logout"),
    path("accounts/password_change/", views.password_change, name="password_change"),
    path("accounts/password_reset/", views.password_reset, name="password_reset"),
    path(
        "accounts/password_reset_done/",
        views.password_reset_done,
        name="password_reset_done",
    ),
    path(
        "accounts/password_reset_from_key/",
        views.password_reset_from_key,
        name="password_reset_from_key",
    ),
    path(
        "accounts/password_reset_from_key_done/",
        views.password_reset_from_key_done,
        name="password_reset_from_key_done",
    ),
    path("accounts/password_set/", views.password_set, name="password_set"),
    path("accounts/sign_in/", views.sign_in, name="account_sign_in"),
    path("accounts/signup/", views.signup, name="account_signup"),
    path("accounts/signup_closed/", views.signup_closed, name="signup_closed"),
    path(
        "accounts/verification_sent/", views.verification_sent, name="verification_sent"
    ),
    path(
        "accounts/verified_email_required/",
        views.verified_email_required,
        name="verified_email_required",
    ),
    #    path( 'set_webhook/', set_webhook ),
    #    path('webhook/', webhook, name='webhook'),
    #    path('telegram_bot/', telegram_bot, name='telegram_bot'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
