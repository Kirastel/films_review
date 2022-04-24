from django.db.models import Q
from .anotations import annotated_actors, annotated_writers, annotated_directors, annotated_films


def search(q, category):
    if category == 'film':
        results = annotated_films.filter(title__icontains=q)

    elif category == 'country':
        results = annotated_films.filter(country__name__icontains=q)

    elif category == 'director':
        results = annotated_directors.filter(
            Q(director__in=annotated_directors.filter(full_name__icontains=q)) |
            Q(director__in=annotated_directors.filter(short_name__icontains=q))
        )
    elif category == 'writer':
        results = annotated_films.filter(
            Q(writer__in=annotated_writers.filter(full_name__icontains=q)) |
            Q(writer__in=annotated_writers.filter(short_name__icontains=q))
        )
    elif category == 'actor':
        results = annotated_actors.filter(
            Q(actor__in=annotated_actors.filter(full_name__icontains=q)) |
            Q(actor__in=annotated_actors.filter(short_name__icontains=q))
        )

    elif category == 'genre':
        results = annotated_films.filter(genres__name__icontains=q)

    elif category == 'year':
        results = annotated_films.filter(release_date__year=q)

    elif category == 'any':
        results = annotated_films.filter(
            Q(title__icontains=q) |
            Q(director__in=annotated_directors.filter(full_name__icontains=q)) |
            Q(director__in=annotated_directors.filter(short_name__icontains=q)) |
            Q(writer__in=annotated_writers.filter(full_name__icontains=q)) |
            Q(writer__in=annotated_writers.filter(short_name__icontains=q)) |
            Q(actor__in=annotated_actors.filter(full_name__icontains=q)) |
            Q(actor__in=annotated_actors.filter(short_name__icontains=q)) |
            Q(genres__name__icontains=q) |
            Q(release_date__year=q)
        )

    else:
        results = annotated_films.none()

    return results.order_by('-avg_rating', 'title')
