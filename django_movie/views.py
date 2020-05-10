from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, View

from django_movie.models import Movie


class MovieList(ListView):
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'
    model = Movie
    context_object_name = 'movies_list'


class MovieDetail(View):
    def get(self, request, slug):
        movie = Movie.objects.get(url=slug)
        return render(request, "movies/movie_detail.html", {"movie": movie})
