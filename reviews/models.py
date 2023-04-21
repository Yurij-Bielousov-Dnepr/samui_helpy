# models.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from offer.models import Helper


# Re_view - для отзыва на помошника
class Re_view(models.Model):
    RATING_CHOICES = (
        (1, "1 звезда"),
        (2, "2 звезды"),
        (3, "3 звезды"),
        (4, "4 звезды"),
        (5, "5 звезд"),
    )

    LEVEL_CHOICES = [
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
    ]

    TAG_CHOICES = [
        ("moto_rent", _("Moto Rent")),
        ("moto_beginner", _("Moto Beginner")),
        ("moto_sos", _("Moto SOS")),
        ("rent_estate", _("Rent Estate")),
        ("public_serv", _("Public Service")),
        ("lang_schol", _("Language School")),
        ("trabl", _("Travel")),
        ("med_help", _("Medical Help")),
        ("serv_transl", _("Translation Services")),
        ("shopping_destination", _("Shopping Destination")),
        ("clothing", _("Clothing")),
        ("food", _("Food")),
        ("souvenirs", _("Souvenirs")),
        ("ind_tour", _("Individual Tour")),
        ("escort", _("Escort")),
    ]

    reviewer_name = models.CharField(max_length=255)
    helper_name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    tag = models.CharField(choices=TAG_CHOICES, max_length=50, blank=False)
    level_of_service = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    review_text = models.TextField()
    wishes = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.helper_name} by {self.reviewer_name}"

    # Review - для отзыва на статью или событие


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1 звезда"),
        (2, "2 звезды"),
        (3, "3 звезды"),
        (4, "4 звезды"),
        (5, "5 звезд"),
    )
    helper = models.ForeignKey(Helper, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
