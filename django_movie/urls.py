from django.urls import path
from django_movie.views import MovieList
app_name = 'django_movie'
urlpatterns = [
    path('', MovieList.as_view(), name='movies_list')
]