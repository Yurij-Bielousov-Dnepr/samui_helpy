# models.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Tag_article(models.Model):
    name = [
        ("moto_rent", _("Moto Rent")),
        ("moto_beginner", _("Moto Beginner")),
        ("moto_sos", _("Moto SOS")),
        ("rent_estate", _("Rent Estate")),
        ("public_serv", _("Public Service")),
        ("lang_schol", _("Language School")),
        ("med_help", _("Medical Help")),
        ("serv_transl", _("Translation Services")),
        ("shopping_destination", _("Shopping Destination")),
        ("souvenirs", _("Souvenirs")),
    ]

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=75)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag_article, verbose_name="Tags")
    is_approved = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag_article)
    is_approved = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, blank=True
    )
    is_favorite = models.BooleanField(default=False)


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, blank=True
    )
    is_favorite = models.BooleanField(default=False)


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1 звезда"),
        (2, "2 звезды"),
        (3, "3 звезды"),
        (4, "4 звезды"),
        (5, "5 звезд"),
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    relevance = models.IntegerField(choices=RATING_CHOICES, verbose_name="Актуальность")
    engagement = models.IntegerField(
        choices=RATING_CHOICES, verbose_name="Увлекательность"
    )
