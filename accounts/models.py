# models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from art_event.models import Favorites, Event, Article
from helpy.models import Region, Language
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError('Email обязателен для создания пользователя.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    userNick = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=255,
        choices=[("Helper", "Helper"), ("Customer", "Customer")],
        default="Customer",
    )
    district = models.ManyToManyField('Region')
    languages = models.ManyToManyField('Language')
    is_sponsor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    about_me = models.TextField(blank=True)

    USERNAME_FIELD = 'userNick'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.userNick

    def get_short_name(self):
        return self.userNick

    @property
    def is_authenticated(self):
        return True if self.id else False

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



User = get_user_model()

class Stats(models.Model):
    date = models.DateField(auto_now_add=True)
    active_helpers = models.IntegerField(default=0)
    help_requests = models.IntegerField(default=0)
    online_users = models.IntegerField(default=0)
    last_activity = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Stats"

    def __str__(self):
        return f"{self.date} - Active helpers: {self.active_helpers}, Help requests: {self.help_requests}, Online users: {self.online_users}"

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name


class Region(models.Model):
    CHAWENG = "Chaweng"
    LAMAI = "Lamai"
    LIPA_NOI = "Lipa Noi"
    NATHON = "Nathon"
    BANG_BOR = "Bang Bor"
    MAENAM = "Maenam"
    BOPHUT = "Bophut"
    CHOENG_MON = "Choeng Mon"
    HUA_THANON = "Hua Thanon"

    REGION_CHOICES = [
        ("", "Choose all"),  # добавляем пустой элемент
        (CHAWENG, "Chaweng"),
        (LAMAI, "Lamai"),
        (LIPA_NOI, "Lipa Noi"),
        (NATHON, "Nathon"),
        (BANG_BOR, "Bang Bor"),
        (MAENAM, "Maenam"),
        (BOPHUT, "Bophut"),
        (CHOENG_MON, "Choeng Mon"),
        (HUA_THANON, "Hua Thanon"),
    ]

    name = models.CharField(max_length=255, choices=REGION_CHOICES)

    def __str__(self):
        return self.name


class Language(models.Model):
    UKRAINIAN = "uk"
    THAI = "th"
    ENGLISH = "en"
    FRENCH = "fr"
    ITALIAN = "it"
    GERMAN = "de"
    RUSSIAN = "ru"

    LANGUAGE_CHOICES = [
        (UKRAINIAN, "Українська"),
        (THAI, "ไทย"),
        (ENGLISH, "English"),
        (FRENCH, "Français"),
        (ITALIAN, "Italiano"),
        (GERMAN, "Deutsch"),
        (RUSSIAN, "Русский"),
    ]

    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return self.language


class SupportLevel(models.Model):
    LEVEL_CHOICES = [
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self):
        return f"Level {self.level}"


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, blank=True
    )
    is_favorite = models.BooleanField(default=False)


class Level(models.Model):
    LEVEL_CHOICES = [
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self):
        return f"Level {self.level}"
