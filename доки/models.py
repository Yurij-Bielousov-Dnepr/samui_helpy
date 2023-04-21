# models.py
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    tags = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    tags = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)


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


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Helper(models.Model):
    name = models.CharField(max_length=255)
    vip = models.BooleanField(default=False)  # add this line
    tags = models.ManyToManyField(Tag)
    support_level = models.IntegerField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    contacts = models.TextField()

    def __str__(self):
        return self.name


# Краткое описание полей:


# name - имя помощника-спонсора
# tags - теги, связь многие ко многим с моделью Tag
# support_level - уровень поддержки (например, от 1 до 5)
# region - район, связь один ко многим с моделью Region
# contacts - контактная информация помощника-спонсора
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


class HelpRequest(models.Model):
    user_nick = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    problem_description = models.TextField()
    district = models.CharField(max_length=255)
    level = models.IntegerField()
    languages = models.ManyToManyField(Language, blank=True)
    contacts = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
