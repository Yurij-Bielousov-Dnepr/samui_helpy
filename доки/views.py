# views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Article, Event, Helper
from .forms import ArticleForm, EventForm, HelperForm


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect("article_detail", pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, "helpy/event_article/add_article.html", {"form": form})


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
        form = HelperForm(request.POST)
        if form.is_valid():
            helper = form.save()
            return redirect("helper_detail", pk=helper.pk)
    else:
        form = HelperForm()
    return render(request, "helpy/add_helper.html", {"form": form})


def events(request):
    events = Event.objects.order_by("date")[:3]
    context = {"events": events}
    return render(request, "helpy/event_article/events.html", context)


def index(request):
    return render(request, "helpy/index.html")


def help(request):
    return render(request, "help.html")


def offer_help(request):
    return render(request, "helpy/offer/offer_help.html")


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
