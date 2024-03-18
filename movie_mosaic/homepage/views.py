from django.shortcuts import get_object_or_404, render
from cinema.models import *
from cinema.forms import *
from django.http import HttpResponse
import random

def index(request):
    template_name = 'homepage/index.html'
    movies_list = VideoProduct.objects.all().order_by('-created_at')
    context = {
        'movies': movies_list
    }
    return render(request, template_name, context)

def post_detail(request, pk):
    template_name = 'homepage/detail.html'
    movies_list = get_object_or_404(
        VideoProduct.objects.values('title', 'original_title__title', 'descriptions', 'image', 'release_year__year',), pk=pk)
    actors = VideoProduct.objects.get(pk=pk).actors.all()
    actor_names = [actor.full_name for actor in actors]
    context = {
        'movies': movies_list,
        'actors': actor_names
    }
    return render(request, template_name, context)

def genres(request, genre):
    template_name = 'homepage/genre.html'
    movies_list = VideoProduct.objects.filter(product_type__title=genre).order_by('-created_at')
    context = {
        'movies': movies_list,
        'genres': genre
    }
    return render(request, template_name, context)

def years(request, year):
    template_name = 'homepage/year.html'
    movies_list = VideoProduct.objects.filter(release_year__year=year).order_by('-created_at')
    context = {
        'movies': movies_list,
        'years': year
    }
    return render(request, template_name, context)

def random_movie(request):
    template_name = 'homepage/random_movie.html'
    form = GenreForm(request.POST or None)
    random_movie = None

    if form.is_valid():
        genre = form.cleaned_data['genre']
        movies = VideoProduct.objects.filter(product_type__title=genre)
        if movies.exists():
            random_movie = random.choice(movies)
    context = {
            'form': form,
            'random_movie': random_movie
            }
    return render(request, template_name, context)

def select_movie(request):
    template_name = 'homepage/select_movie.html'
    form = GenreForm(request.POST or None)
    select_movies = []
    genre = ''

    if form.is_valid():
        genre = form.cleaned_data['genre']
        movies = VideoProduct.objects.filter(product_type__title=genre).order_by('-created_at')
        if movies.exists():
            select_movies = movies
    context = {
            'form': form,
            'select_movies': select_movies,
            'genres': genre
            }
    return render(request, template_name, context )