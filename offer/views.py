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
from helpy.forms import *
from accounts.models import *
from .models import *
from helpy.models import *
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

    return render(request, "helpy/offer/helper_form.html", context)


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
    return render(request, "helpy/offer/success.html")


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


def add_helper(request):
    if request.method == "POST":
        form = HelpForm(request.POST)
        if form.is_valid():
            helper = form.save()
            return redirect("helper_detail", pk=helper.pk)
    else:
        form = HelpForm()
    return render(request, "helpy/add_helper.html", {"form": form})


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
