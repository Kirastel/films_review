from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.contrib.auth.decorators import login_required
from . import views
import debug_toolbar
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'films_review'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),

    path('published_films/', views.FilmsListView.as_view(),
         name='films_list'),
    re_path(r'^film/(?P<pk>\d+)-(?P<slug>[\w-]+)/$',
            views.FilmDetailView.as_view(),
            name='film'),

    path('search/', views.SearchListView.as_view(), name='search'),

    re_path(r'^review/(?P<pk>\d+)-(?P<slug>[\w-]+)/add/$',
            login_required(views.ReviewCreateView.as_view()),
            name='add_review'),
    re_path(r'^review/(?P<pk>\d+)-(?P<slug>[\w-]+)/edit/$',
            login_required(views.ReviewUpdateView.as_view()),
            name='edit_review'),
    re_path(r'^review/(?P<pk>\d+)-(?P<slug>[\w-]+)/delete/$',
            login_required(views.ReviewDeleteView.as_view()),
            name='delete_review'),
    path('my_reviews/',
         login_required(views.MyReviewsListView.as_view()),
         name='my_reviews'),
]

# if settings.DEBUG:
#     urlpatterns = [
#                 path('__debug__/', include(debug_toolbar.urls)),
#                   ] + urlpatterns


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
