# views.py
# from .forms import HelperForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView
from .decorators import admin_only
from .forms import *
from .models import *


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
    return render(request, "art_event/add_review.html", {"form": form})
