from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, View
from .forms import FormReview
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

