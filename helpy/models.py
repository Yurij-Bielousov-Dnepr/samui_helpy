# models.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


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


class Tag_help(models.Model):
    name_choices = (
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
    )
    name = models.CharField(
        max_length=255, choices=name_choices, verbose_name=_("Name")
    )

    class Meta:
        verbose_name = _("Tag_help")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


def __str__(self):
    return self.name


class Level(models.Model):
    LEVEL_CHOICES = [
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self):
        return f"Level {self.level}"


class HelpRequest(models.Model):
    user_nick = models.CharField(max_length=55, blank=False, null=False)
    category = models.ForeignKey(Tag_help, on_delete=models.CASCADE, default=1)
    problem_description = models.TextField(
        max_length=255, blank=False, null=False, default="-= =-"
    )
    district = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, default=1)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, default=1)
    contacts = models.CharField(
        max_length=255, blank=False, null=False, default="12345"
    )

    def __str__(self):
        return self.problem_description[:50]


class HelpRequestLanguage(models.Model):
    help_request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)


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
