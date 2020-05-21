from django.urls import path
from django_movie.views import MovieList, MovieDetail, AddReview, ActorsView

app_name = 'django_movie'
urlpatterns = [
    path('', MovieList.as_view(), name='movies_list'),
    path("<slug:slug>/", MovieDetail.as_view(), name='movie_detail'),
    path('review<int:pk>', AddReview.as_view(), name='add_review'),
    path("actor/<str:slug>/", ActorsView.as_view(), name="actor_detail"),
]
