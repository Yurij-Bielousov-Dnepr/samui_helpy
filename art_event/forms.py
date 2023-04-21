from django import forms
from django.utils.translation import gettext as _
from .models import Article, Event, Helper, HelpRequest, Language, Review, Tag_article
from .models import Tag_help, SupportLevel, Region, Re_view, Level
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.urls import reverse_lazy
from django.views.generic import CreateView


class DeleteProfileForm(forms.Form):
    confirm = forms.BooleanField(
        label=_("Confirm deletion"),
        help_text=_(
            "Are you sure you want to delete your profile? This cannot be undone."
        ),
        required=True,
    )


class VIPServicesForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True,
    )
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=50,
        required=True,
    )
    phone = forms.CharField(
        label=_("Phone"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=20,
        required=True,
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=True,
    )


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=Re_view.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    level_of_service = forms.ChoiceField(
        choices=Re_view.LEVEL_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-control"}),
    )
    review_text = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    wishes = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    tag = forms.ChoiceField(
        choices=Re_view.TAG_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Re_view
        fields = [
            "reviewer_name",
            "helper_name",
            "tag",
            "rating",
            "level_of_service",
            "review_text",
            "wishes",
        ]
        widgets = {
            "reviewer_name": forms.TextInput(attrs={"class": "form-control"}),
            "helper_name": forms.TextInput(attrs={"class": "form-control"}),
            "rating": forms.RadioSelect(attrs={"class": "form-control"}),
            "tag": forms.Select(attrs={"class": "form-control"}),
            "level_of_service": forms.RadioSelect(attrs={"class": "form-control"}),
            "review_text": forms.TextInput(attrs={"class": "form-control"}),
            "wishes": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        reviewer_name = cleaned_data.get("reviewer_name")
        helper_name = cleaned_data.get("helper_name")
        rating = cleaned_data.get("rating")
        tag = cleaned_data.get("tag")
        level_of_service = cleaned_data.get("level_of_service")
        review_text = cleaned_data.get("review_text")
        wishes = cleaned_data.get("wishes")
        if (
            not reviewer_name
            or not helper_name
            or not rating
            or not tag
            or not level_of_service
            or not review_text
        ):
            raise forms.ValidationError(
                "All fields are required", code="required_fields"
            )


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ["language"]
        widgets = {
            "language": forms.CheckboxSelectMultiple,
        }


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ["name"]
        widgets = {
            "name": forms.CheckboxSelectMultiple,
        }


# Это предупреждение, а не ошибка. Оно связано с тем, что ваша форма TagForm наследуется от forms.ModelForm,
# который уже имеет базовый класс ModelForm и метакласс ModelFormMetaclass. Поэтому вы можете опустить указание метакласса
# в вашем коде. Попробуйте изменить первую строку на следующую:
# class TagForm(forms.ModelForm):


class Tag_helpForm(forms.ModelForm):
    class Meta:
        model = Tag_help
        fields = ["name"]
        labels = {"name": _("Name")}


class SupportLevelForm(forms.ModelForm):
    class Meta:
        model = SupportLevel
        fields = ["level"]
        widgets = {
            "level": forms.CheckboxSelectMultiple(),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["customer_name", "rating", "comment"]
        labels = {
            "customer_name": _("Helper Nickname"),
            "rating": _("Rate"),
            "comment": _("Comment"),
        }
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "tags"]

        widgets = {
            "content": forms.Textarea(),
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "checkbox"}),
        }


class EventCreationForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.CharField(max_length=5, widget=forms.TimeInput(format="%H:%M"))
    location = forms.CharField(max_length=255)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag_article.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Event
        fields = ["title", "description", "date", "time", "location", "tags"]


class EventCreateView(CreateView):
    model = Event
    template_name = "helpy/event_article/add_event.html"
    form_class = EventCreationForm
    success_url = reverse_lazy("events")


class HelpForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = [
            "user_nick",
            "category",
            "problem_description",
            "district",
            "level",
            "language",
            "contacts",
        ]

        widgets = {
            "language": forms.CheckboxSelectMultiple(
                attrs={"class": "inline-checkbox"}
            ),
            "level": forms.RadioSelect(attrs={"class": "inline-radio"}),
            "category": forms.SelectMultiple(attrs={"size": 15}),
            "district": forms.SelectMultiple(attrs={"size": 9}),
        }

    user_nick = forms.CharField(label="User Nickname")
    category = forms.ModelChoiceField(
        queryset=Tag_help.objects.all(), label="Category", widget=forms.Select
    )
    problem_description = forms.CharField(label="Describe problem")
    district = forms.ModelChoiceField(
        queryset=Region.objects.all(), label="District", widget=forms.Select
    )
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(), label="Level", widget=forms.RadioSelect
    )
    language = forms.MultipleChoiceField(
        choices=Language.LANGUAGE_CHOICES,
        label="Language",
        widget=forms.CheckboxSelectMultiple,
    )
    contacts = forms.CharField(label="Contacts")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "language" in self.fields:
            language_choices = dict(Language.LANGUAGE_CHOICES)
            self.fields["language"].widget = forms.CheckboxSelectMultiple(
                attrs={"class": "inline-checkbox"}
            )
            self.fields["language"].choices = [
                (code, language_choices[code]) for code in language_choices
            ]


class HelpRequestForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = HelpRequest
        fields = [
            "user_nick",
            "category",
            "problem_description",
            "district",
            "level",
            "contacts",
            "languages",
        ]
        labels = {
            "user_nick": _("User Nickname"),
            "category": _("Category"),
            "problem_description": _("Describe the problem"),
            "district": _("District"),
            "level": _("Level"),
            "contacts": _("Contacts"),
            # 'tags': _('Tags (up to 3)'),
        }


# forms.py
class HelperCreateForm(forms.ModelForm):
    user_type = forms.CharField(widget=forms.HiddenInput(), initial="helper")

    class Meta:
        model = Helper
        fields = (
            "name",
            "user_offer_is_free",
            "tags",
            "support_levels",
            "regions",
            "contacts",
            "languages",
            "email",
            "phone",
        )
        labels = {
            "user_offer_is_free": "Free offer",
            "name": "Name",
            "tags": "Tags",
            "support_levels": "Support levels",
            "regions": "Regions",
            "contacts": "Contacts",
            "languages": "Languages",
            "email": "Email",
            "phone": "Phone",
        }
        widgets = {
            "tags": forms.CheckboxSelectMultiple,
            "support_levels": forms.CheckboxSelectMultiple,
            "regions": forms.CheckboxSelectMultiple,
            "language": forms.CheckboxSelectMultiple(
                attrs={"class": "inline-checkbox"}
            ),
        }
        # Add the following line to define the soft_skills field
        soft_skills = forms.CharField(
            required=False, label="Soft skills", widget=forms.Textarea
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "language" in self.fields:
            language_choices = dict(Language.LANGUAGE_CHOICES)
            self.fields["language"].widget = forms.CheckboxSelectMultiple(
                attrs={"class": "inline-checkbox"}
            )
            self.fields["language"].choices = [
                (code, language_choices[code]) for code in language_choices
            ]


class HelperUpdateForm(forms.ModelForm):
    class Meta:
        model = Helper
        fields = (
            "name",
            "user_offer_is_free",
            "tags",
            "support_levels",
            "regions",
            "contacts",
            "languages",
            "email",
            "soft_skills",
            "phone",
        )
        labels = {
            "user_offer_is_free": _("Free offer"),
            "name": _("Name"),
            "tags": _("Tags"),
            "support_levels": _("Support levels"),
            "regions": _("District"),
            "contacts": _("Contacts"),
            "languages": _("Languages"),
            "email": _("Email"),
            "soft_skills": _("soft_skills"),
            "phone": _("Phone"),
        }
        widgets = {
            "tags": forms.CheckboxSelectMultiple,
            "support_levels": forms.CheckboxSelectMultiple,
            "regions": forms.CheckboxSelectMultiple,
            "languages": forms.CheckboxSelectMultiple,
        }
