from django.urls import path
from django_movie.views import MoviesView, MovieDetail, AddReview, ActorsView, FilterMoviesView

app_name = 'django_movie'
urlpatterns = [
    path('', MoviesView.as_view()),
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path("<slug:slug>/", MovieDetail.as_view(), name='movie_detail'),
    path('review<int:pk>', AddReview.as_view(), name='add_review'),
    path("actor/<str:slug>/", ActorsView.as_view(), name="actor_detail"),
]
