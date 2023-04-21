# views.py
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import DeleteView

# from .forms import HelperForm
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView
from django_countries import countries
from accounts.models import Stats
from offer.models import Helper
from .forms import *
from .models import *
from .my_menu import *


def my_view(request):
    menu_items = get_menu_items()
    context = {
        "menu_items": menu_items,
    }
    return render(request, "base_templates/header.html", context)


class HelpMyView(LoginRequiredMixin, View):
    template_name = "helpy/helpmy.html"
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
                "helpy/help.html",
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
    template_name = "offer/helper_form.html"
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

    return render(request, "offer/helper_form.html", context)


def helper_form(request):
    if request.method == "POST":
        form = HelperCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Helper added successfully!")
            return redirect("success")
    else:
        form = HelperCreateForm()
    return render(request, "offer/helper_form.html", {"form": form})


def success(request):
    return render(request, "offer/success.html")


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
    return render(request, "helpy/helpmy.html", context)


# Классы-представления для помощников (Helper)
class HelperListView(ListView):
    model = Helper
    template_name = "offer/helper_list.html"
    context_object_name = "helpers"


class HelperDeleteView(LoginRequiredMixin, DeleteView):
    model = Helper
    success_url = reverse_lazy("helper_list")
    template_name = "offer/helper_confirm_delete.html"

    def get_object(self):
        return get_object_or_404(Helper, pk=self.kwargs["pk"], user=self.request.user)


def add_helper(request):
    if request.method == "POST":
        form = HelpForm(request.POST)
        if form.is_valid():
            helper = form.save()
            return redirect("helper_detail", pk=helper.pk)
    else:
        form = HelpForm()
    return render(request, "helpy/add_helper.html", {"form": form})


def index(request):
    return render(request, "index.html")


class HelperUpdateView(LoginRequiredMixin, UpdateView):
    model = Helper
    form_class = HelperUpdateForm
    template_name = "offer/update_helper.html"
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
