import datetime
from itertools import chain
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic
from django.http import Http404
from .models import Film, Review
from films_review.custom.anotations import annotated_films
from films_review.custom import constants
from films_review.custom.search import search
from .forms import SearchForm


class IndexListView(generic.list.ListView):
    template_name = 'films_review/index.html'
    context_object_name = 'last_reviewed'
    paginate_by = 5

    def get_queryset(self):
        today = datetime.date.today()
        last_reviewed = annotated_films.filter(id__lt=2)  # нужно сделать чтобы подтягивал из бд свежие обзоры на фильм
        return last_reviewed


class FilmsListView(generic.list.ListView):
    template_name = 'films_review/films_list.html'
    context_object_name = 'films'
    paginate_by = 5

    def get(self, *args, **kwargs):
        if self.request.GET.get('order') is None:
            return redirect(reverse('films_review:films_list') + '?order=recent')
        return super().get(*args, **kwargs)

    def get_queryset(self):
        today = datetime.date.today()
        published_films = annotated_films.filter(post_date__lte=today)
        order_dict = {
            'recent': '-post_date',
            'popular': '-num_reviews',
            'best_rated': '-avg_rating',
        }
        order_key = self.request.GET.get('order')
        order_value = order_dict.get(order_key)
        if order_value is None:
            raise Http404
        return published_films.order_by(order_value, 'title')


class FilmDetailView(generic.detail.DetailView):
    model = Film
    template_name = 'films_review/film_details.html'
    context_object_name = 'film'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(film=context.get('film')).order_by('-post_date')
        user = self.request.user if self.request.user.is_authenticated else None
        user_review = reviews.filter(owner=user).first()

        if user_review:
            other_reviews = reviews.exclude(owner=user)
            reviews = list(chain((user_review,), other_reviews))

        paginator = Paginator(reviews, constants.REVIEWS_PER_PAGE)
        page_number = self.request.GET.get('page', '1')
        page_obj = paginator.get_page(page_number)

        context.update({
            'paginator': paginator,
            'page_obj': page_obj,
            'is_paginated': True,
            'reviews': reviews,
        })
        return context


class ReviewCreateView(generic.edit.CreateView):
    model = Review
    fields = ['rating', 'title', 'text']
    template_name = 'films_review/review/add_review.html'

    def get(self, request, *args, **kwargs):
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        films_reviews = film.review_set.all()
        users_already_reviewed = User.objects.filter(review__in=films_reviews)

        if not film.is_released() or request.user in users_already_reviewed:
            return redirect(film)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        context.update({
            'film': film,
        })
        return context

    def form_valid(self, form):
        new_review = form.save(commit=False)
        new_review.owner = self.request.user
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        new_review.film = film
        return super().form_valid(form)

    def get_success_url(self):
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        return film.get_absolute_url()


class ReviewUpdateView(generic.edit.UpdateView):
    fields = ['rating', 'title', 'text']
    template_name = 'films_review/review/edit_review.html'

    def get_object(self, queryset=None):
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        review = get_object_or_404(Film, film=film, owner=self.request.user)
        return review

    def get_success_url(self):
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        return film.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        context.update({
            'film': film
        })
        return context


class ReviewDeleteView(generic.edit.DeleteView):
    template_name = 'films_review/review/delete_review.html'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        review = get_object_or_404(Review, film=film, owner=self.request.user)
        return review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        context.update({
            'film': film
        })
        return context

    def get_success_url(self):
        film = get_object_or_404(Film, id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        return film.get_absolute_url()


class MyReviewsListView(generic.list.ListView):
    template_name = 'films_review/review/my_reviews.html'
    context_object_name = 'my_reviews'
    paginate_by = constants.REVIEWS_PER_PAGE

    def get_queryset(self):
        return Review.objects.filter(owner=self.request.user).order_by('-post_date', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SearchListView(generic.list.ListView):
    def get(self, request, *args, **kwargs):
        form = SearchForm(data=request.GET)

        if form.is_valid():
            return super().get(request, *args, **kwargs)
        elif form.data.get('q') is None:
            return render(request, 'films_review/search/empty_search.html')
        else:
            return render(request, 'films_review/search/wrong_search.html')

    def get_queryset(self):
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        results = search(q=q, category=category)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'q': self.request.GET.get('q'),
            'category': self.request.GET.get('category'),
            'SEARCH_CATEGORIES': constants.SEARCH_CATEGORIES,
        })
        return context
