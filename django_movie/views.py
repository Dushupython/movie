from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, View, DetailView
from .forms import FormReview
from django_movie.models import Movie, Actors, Genre


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_year(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'
    context_object_name = 'movie_list'


class MovieDetail(GenreYear, View):
    def get(self, request, slug):
        movie = Movie.objects.get(url=slug)
        return render(request, "movies/movie_detail.html", {"movie": movie})


class AddReview(View):
    def post(self, request, pk):
        form = FormReview(request.POST)
        mov = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = mov
            form.save()
        return redirect(mov.get_absolute_url())


class ActorsView(GenreYear, DetailView):
    model = Actors
    template_name = 'movies/actors.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(year__in=self.request.GET.getlist("year"))
        return queryset

