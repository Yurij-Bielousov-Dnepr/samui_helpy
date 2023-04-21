# views.py
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django_countries import countries
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .decorators import admin_only
from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# from .forms import HelperForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from .my_menu import *
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views import View


def my_view(request):
    menu_items = get_menu_items()
    context = {
        "menu_items": menu_items,
    }
    return render(request, "header.html", context)


class VIPView(TemplateView):
    template_name = "helpy/VIP.html"


@method_decorator(login_required, name="dispatch")
class VIPServicesView(TemplateView):
    template_name = "helpy/VIP.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = VIPServicesForm()
        return context

    def post(self, request, *args, **kwargs):
        form = VIPServicesForm(request.POST)
        if form.is_valid():
            # Process the form data
            # ...
            return render(request, "success.html")
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)


@method_decorator(staff_member_required, name="dispatch")
class ReviewUpdateView(UpdateView):
    model = Review
    fields = ["is_approved"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("moderate")


@method_decorator(staff_member_required, name="dispatch")
class ModerateView(ListView):
    model = Review
    template_name = "helpy/moderation.html"
    context_object_name = "reviews"

    def get_queryset(self):
        return Review.objects.filter(is_approved="0")


# тут надо разобраться модернизировать вьюху чтобы она модерила все: статьи, события и отзывы


@user_passes_test(lambda u: u.is_staff)
def moderation(request):
    articles = Article.objects.filter(is_approved=False)
    events = Event.objects.filter(is_approved=False)
    reviews = Review.objects.filter(is_approved=False)

    if request.method == "POST":
        for obj in articles:
            action = request.POST.get("action_{}".format(obj.id))
            if action == "approve":
                obj.is_approved = True
                obj.save()
            elif action == "delete":
                obj.delete()
            elif action == "edit":
                return redirect("article_edit", obj.pk)

        for obj in events:
            action = request.POST.get("action_{}".format(obj.id))
            if action == "approve":
                obj.is_approved = True
                obj.save()
            elif action == "delete":
                obj.delete()
            elif action == "edit":
                return redirect("update_event", pk=obj.pk)

        for obj in reviews:
            action = request.POST.get("action_{}".format(obj.id))
            if action == "approve":
                obj.is_approved = True
                obj.save()
            elif action == "delete":
                obj.delete()
            elif action == "edit":
                return redirect("review_edit", obj.pk)

        return redirect("moderation")

    context = {
        "articles": articles,
        "events": events,
        "reviews": reviews,
    }
    return render(request, "helpy/moderation.html", context)


class ReviewCreateView(CreateView):
    model = Re_view
    form_class = ReviewForm
    template_name = "helpy/reviews/review_add.html"
    success_url = reverse_lazy("reviews:thanks")

    def form_valid(self, form):
        review = form.save(commit=False)
        review.reviewer_name = form.cleaned_data.get("reviewer_name")
        review.helper_name = form.cleaned_data.get("helper_name")
        review.rating = form.cleaned_data.get("rating")
        review.tag = form.cleaned_data.get("tag")
        review.level_of_service = form.cleaned_data.get("level_of_service")
        review.review_text = form.cleaned_data.get("review_text")
        review.wishes = form.cleaned_data.get("wishes")
        review.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        return context


def review_helper(request):
    context = {
        "page_title": _("User Reviews"),
        "page_description": _(
            "User reviews are important for evaluating the quality and usability of the website. Sorting and adding reviews are important components of the user experience. They allow users to quickly find the information they need and share their opinion. It is important to ensure the security of reviews by checking for spam and moderation."
        ),
        "add_review_url": "reviews_add",
        "reviews_list_url": "reviews_list",
    }
    return render(request, "helpy/reviews/review_helper.html", context)


def review_list_helper(request):
    reviews = Re_view.objects.all()

    sort_by = request.GET.get("sort", "rating")
    sort_order = request.GET.get("order", "desc")

    if sort_order == "desc":
        sort_by = f"-{sort_by}"

    reviews = reviews.order_by(sort_by)

    paginator = Paginator(reviews, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "reviews": page_obj,
        "sort_by": sort_by,
    }
    return render(request, "helpy/reviews/reviews_list.html", context)


def review_detail(request, pk):
    review = get_object_or_404(Re_view, pk=pk)
    context = {
        "review": review,
    }
    return render(request, "helpy/reviews/review_detail.html", context)


class HelpMyView(LoginRequiredMixin, View):
    template_name = "helpy/help/helpmy.html"
    form_class = HelpRequestForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={"userNick": request.user.username})
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            userNick = form.cleaned_data["userNick"]
            category = form.cleaned_data["category"]
            problemDescription = form.cleaned_data["problemDescription"]
            district = form.cleaned_data["district"]
            level = form.cleaned_data["level"]
            free_helpers = Helper.objects.filter(
                Q(tags__name__in=category) | Q(languages__name__in=category),
                region=district,
                support_level__gte=level,
                user_offer_is_free=True,
            ).order_by("-vip", "?")
            paginator = Paginator(free_helpers, 9)  # 9 results per page
            page = request.GET.get("page")
            free_helpers = paginator.get_page(page)
            help_requests_count = HelpRequest.objects.all().count()
            active_helpers_count = Helper.objects.filter(
                user_offer_is_free=True
            ).count()
            stats = Stats.objects.get(date=date.today())
            online_users_count = stats.online_users
            return render(
                request,
                "helpy/help/help.html",
                {
                    "form": form,
                    "free_helpers": free_helpers,
                    "active_helpers_count": active_helpers_count,
                    "help_requests_count": help_requests_count,
                    "online_users_count": online_users_count,
                },
            )
        else:
            return render(request, self.template_name, {"form": form})


@login_required
class CreateHelper(CreateView):
    model = Helper
    form_class = HelperCreateForm
    template_name = "helpy/offer/create_helper.html"
    success_url = reverse_lazy("helper_profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.user_type = "helper"
        messages.success(
            self.request, _("Your helper data has been created successfully.")
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Please correct the errors below."))
        return super().form_invalid(form)


def add_tag(request):
    if request.method == "POST":
        form = Tag_helpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tags_list")
    else:
        form = Tag_helpForm()

    context = {"form": form}

    # Если форма не прошла валидацию, добавляем в контекст список ошибок
    if form.errors:
        context["errors"] = form.errors

    return render(request, "helpy/offer/helper_form.html", context)


def language_form(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            languages = form.cleaned_data["languages"]
            for language in languages:
                Language.objects.create(language=language)
            return redirect("helper_form")
    else:
        form = LanguageForm()
    return render(request, "helpy/offer/helper_form.html", {"form": form})


def helper_form(request):
    if request.method == "POST":
        form = HelperCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Helper added successfully!")
            return redirect("success")
    else:
        form = HelperCreateForm()
    return render(request, "helpy/offer/helper_form.html", {"form": form})


def success(request):
    return render(request, "helpy/offer/success.html")


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


class LogoutView(auth_views.LogoutView):
    template_name = "accounts/login.html"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        logout(request)
        return redirect("login")


class SignupView(FormView):
    form_class = UserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("index")  # здесь нужно указать URL главной страницы

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        auth_login(self.request, user)  # авторизуем пользователя
        return response

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid form submission.")
            return render(request, self.template_name, {"form": form})


login_view = LoginView.as_view()
logout_view = LogoutView.as_view()
signup_view = SignupView.as_view()


def get_languages_with_flags(languages):
    result = []
    for code, name in languages:
        country = countries.by_code(code)
        if country:
            flag = country.flag
        else:
            flag = ""
        result.append((code, name, flag))
    return result


@admin_only
def moderation_view(request):
    """
    Представление для модерации статей и событий
    """
    articles = Article.objects.filter(is_approved=False)
    events = Event.objects.filter(is_approved=False)
    return render(
        request, "helpy/admin_only.html", {"articles": articles, "events": events}
    )


def review_list(request):
    reviews = Review.objects.all()
    order = request.GET.get("order", "-created_at")
    paginator = Paginator(reviews.order_by(order), 9)
    page = request.GET.get("page")
    reviews = paginator.get_page(page)
    context = {"reviews": reviews, "order": order}
    return render(request, "helpy/event_article/review.html", context=context)


# def helper_detail(request, helper_id):
#     helper = get_object_or_404(Helper, id=helper_id)
#     reviews = Review.objects.filter(helper=helper)
#
#     support_levels = Helper.objects.values_list('support_level', flat=True)
#
#     context = {
#         'helper': helper,
#         'reviews': reviews,
#         'name': helper.name,
#         'tags': helper.tags.all(),
#         'support_levels': support_levels,
#         'region': helper.region,
#         'contacts': helper.contacts,
#         'user_offer_is_free': helper.user_offer_is_free,
#         'user_type': helper.user_type,
#     }
#     return render(request, 'helpy/helper_detail.html', context)


def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            helper_nick = form.cleaned_data["helper_nick"]
            category_help = form.cleaned_data["category_help"]
            problem_description = form.cleaned_data["problem_description"]
            rate = form.cleaned_data["rate"]
            comment = form.cleaned_data["comment"]
            helper = Helper.objects.get(name=helper_nick)
            Review.objects.create(
                helper=helper,
                category_help=category_help,
                problem_description=problem_description,
                rate=rate,
                comment=comment,
            )
            return redirect("reviews")
    else:
        form = ReviewForm()
    return render(request, "helpy/event_article/add_review.html", {"form": form})


def search_helpers(request):
    help_requests = HelpRequest.objects.all()
    search_query = request.GET.get("search")
    tag_query = request.GET.get("tag")
    offer_is_free = request.GET.get("offer_is_free")
    language_query = request.GET.get("language")

    if search_query:
        help_requests = help_requests.filter(user_nick__icontains=search_query)

    if tag_query:
        help_requests = help_requests.filter(category__name__icontains=tag_query)

    if offer_is_free == "true":
        help_requests = help_requests.filter(user_offer_is_free=True)
    elif offer_is_free == "false":
        help_requests = help_requests.filter(user_offer_is_free=False)

    if language_query:
        help_requests = help_requests.filter(
            languages__language__icontains=language_query
        )

    context = {
        "help_requests": help_requests,
        "tags": Tag_help.objects.all(),
    }
    return render(request, "helpmy.html", context)


# Классы-представления для статей (Article)
class ArticleListView(ListView):
    model = Article
    template_name = "helpy/event_article/articles.html"
    context_object_name = "articles"


# def helpmy(request):
#     return render( request, 'helpy/help/helpmy.html' )


class Events(DetailView):
    model = Event
    template_name = "helpy/event_article/events.html"
    context_object_name = "event"


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["events"] = Event.objects.all()
    return context


from .forms import EventCreationForm


class EventCreateView(CreateView):
    model = Event
    template_name = "helpy/event_article/add_event.html"
    form_class = EventCreationForm
    fields = ("title", "description", "date", "location", "tags", "is_favorite")
    success_url = reverse_lazy("events")

    # fields = ( 'Calendar', 'Events Calendar', 'Google Maps',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class EventUpdateView(View):
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        form = EventForm(instance=event)
        return render(request, "event_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_detail", pk=event.pk)
        return render(request, "event_form.html", {"form": form})


class EventDeleteView(DeleteView):
    model = Event
    template_name = "helpy/event_confirm_delete.html"
    success_url = reverse_lazy("events")


@login_required  # Ограничиваем доступ только для авторизованных пользователей
def favorites(request):
    user = request.user
    # Получаем список статей и событий, которые пользователь добавил в избранное
    favorite_articles = Article.objects.filter(favorites=user.profile)
    favorite_events = Event.objects.filter(favorites=user.profile)
    context = {
        "favorite_articles": favorite_articles,
        "favorite_events": favorite_events,
    }
    return render(request, "favorites.html", context)


# Классы-представления для помощников (Helper)
class HelperListView(ListView):
    model = Helper
    template_name = "helpy/offer/helper_list.html"
    context_object_name = "helpers"


class HelperDeleteView(LoginRequiredMixin, DeleteView):
    model = Helper
    success_url = reverse_lazy("helper_list")
    template_name = "helpy/offer/helper_confirm_delete.html"

    def get_object(self):
        return get_object_or_404(Helper, pk=self.kwargs["pk"], user=self.request.user)


def add_article(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            # сохраняем данные из формы в базу данных
            form.save()
            # редиректим пользователя на другую страницу
            return redirect("articles")
    return render(request, "helpy/event_article/add_article.html", {"form": form})


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = "helpy/article_form.html"
    fields = (
        "title",
        "content",
    )
    success_url = reverse_lazy("article_list")


def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect("event_detail", pk=event.pk)
    else:
        form = EventForm()
    return render(request, "helpy/event_article/add_event.html", {"form": form})


def add_helper(request):
    if request.method == "POST":
        form = HelpForm(request.POST)
        if form.is_valid():
            helper = form.save()
            return redirect("helper_detail", pk=helper.pk)
    else:
        form = HelpForm()
    return render(request, "helpy/add_helper.html", {"form": form})


def events(request):
    events = Event.objects.order_by("date")[:3]
    context = {"events": events}
    return render(request, "helpy/event_article/events.html", context)


def index(request):
    return render(request, "helpy/index.html")


# на случай если я решу использовать поиск по помощникам. пока концепция этого не предумсматиривает
# def offer_help(request):
#    return render( request, 'helpy/offer_help.html' )


def articles(request):
    return render(request, "helpy/event_article/articles.html")


def events(request):
    return render(request, "helpy/event_article/events.html")


def about(request):
    return render(request, "helpy/about.html")


def login(request):
    return render(request, "helpy/../templates/account/sign_in.html")


class ArticleFormView:
    def get(self, request, *args, **kwargs):
        return render(request, "helpy/event_article/articles.html")


class ArticleDetailView:
    pass


def donate_view(request):
    return render(request, "donate.html")


def account_inactive(request):
    return render(request, "accounts/account_inactive.html")


def email(request):
    return render(request, "accounts/email.html")


def email_confirm(request):
    return render(request, "accounts/email_confirm.html")


def login(request):
    return render(request, "accounts/login.html")


def logout(request):
    return render(request, "accounts/logout.html")


def password_change(request):
    return render(request, "accounts/password_change.html")


def password_reset(request):
    return render(request, "accounts/password_reset.html")


def password_reset_done(request):
    return render(request, "accounts/password_reset_done.html")


def password_reset_from_key(request):
    return render(request, "accounts/password_reset_from_key.html")


def password_reset_from_key_done(request):
    return render(request, "accounts/password_reset_from_key_done.html")


def password_set(request):
    return render(request, "accounts/password_set.html")


def sign_in(request):
    return render(request, "accounts/sign_in.html")


def signup(request):
    return render(request, "accounts/signup.html")


def signup_closed(request):
    return render(request, "accounts/signup_closed.html")


def verification_sent(request):
    return render(request, "accounts/verification_sent.html")


def verified_email_required(request):
    return render(request, "accounts/verified_email_required.html")


class HelperUpdateView(LoginRequiredMixin, UpdateView):
    model = Helper
    form_class = HelperUpdateForm
    template_name = "helpy/offer/update_helper.html"
    success_url = reverse_lazy("helper_profile")

    def get_object(self):
        return get_object_or_404(Helper, pk=self.kwargs["pk"], user=self.request.user)

    def form_valid(self, form):
        messages.success(
            self.request, "Your helper data has been updated successfully."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
