from urllib import request

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, View, DetailView
from .forms import FormReview, RatingForm
from django_movie.models import Movie, Actors, Genre, Rating


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
        star_form = RatingForm()
        context = {
            "movie": movie,
            'star_form': star_form
        }
        return render(request, "movies/movie_detail.html", context=context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['star_form'] = RatingForm()
    #     return context


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
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist('year')) |
                                        Q(genre__in=self.request.GET.getlist('genre'))
                                        )
        return queryset

    template_name = 'movies/movie_list.html'


class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': request.POST.get('star')}

            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genre__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tag_line", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)