from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from django_movie.models import Movie


class MovieList(ListView):
    template_name = 'movies/movies.html'
    model = Movie
    context_object_name = 'movies_list'
