# models.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Helper(models.Model):
    USER_TYPE_CHOICES = (
        ("helper", "Помощник"),
        ("customer", "Клиент"),
    )
    name = models.CharField(max_length=255)
    vip = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag_help)
    support_levels = models.ManyToManyField(SupportLevel)
    regions = models.ManyToManyField(Region)
    contacts = models.TextField()
    user_offer_is_free = models.BooleanField(default=False)
    languages = models.ManyToManyField(Language)
    email = models.EmailField(max_length=255, blank=True, null=True)
    soft_skills = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
