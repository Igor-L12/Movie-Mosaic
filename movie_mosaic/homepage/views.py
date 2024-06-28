from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from cinema.models import *
from cinema.forms import *
from posts.models import *
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
import random

from games.views import games_index


def index(request):
    # Получаем данные о постах
    post_list = Post.objects.all()
    paginator_posts = Paginator(post_list, 3)
    page_number_posts = request.GET.get('page_posts')
    page_obj_posts = paginator_posts.get_page(page_number_posts)

    # Получаем данные о фильмах с предварительной выборкой рейтингов
    if request.user.is_authenticated:
        user_ratings = Rating.objects.filter(user=request.user)
        movie_list = VideoProduct.objects.filter(moderated=True).order_by('-created_at').prefetch_related(
            Prefetch('rating_set', queryset=user_ratings, to_attr='user_ratings')
        )
    else:
        movie_list = VideoProduct.objects.filter(moderated=True).order_by('-created_at')

    paginator_movies = Paginator(movie_list, 7)
    page_number_movies = request.GET.get('page_movies')
    page_obj_movies = paginator_movies.get_page(page_number_movies)

    page_obj_games = games_index(request)

    # Для каждого фильма получаем рейтинг пользователя из предварительно выбранных данных
    for movie in page_obj_movies:
        if request.user.is_authenticated:
            movie.user_rating = movie.user_ratings[0] if movie.user_ratings else None
        else:
            movie.user_rating = None

    context = {
        'page_obj_posts': page_obj_posts,
        'page_obj_movies': page_obj_movies,
        'page_obj_games': page_obj_games
    }
    
    return render(request, 'cinema/videoproduct_list.html', context)
    

class PostDetailView(DetailView):
    model = VideoProduct
    queryset = VideoProduct.objects.filter()
    template_name = 'homepage/post_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        actors = movie.actors.all()
        actor_names = [actor.full_name for actor in actors]
        context['actors'] = actor_names

        # Получаем рейтинг пользователя для этого фильма
        user_rating = None
        if self.request.user.is_authenticated:
            user_rating_obj = Rating.objects.filter(user=self.request.user, movie=movie).first()
            if user_rating_obj:
                user_rating = user_rating_obj.star.value
        
        context["user_rating"] = user_rating
        context["star_form"] = RatingForm()

    
        # Проверяем, добавлен ли фильм в закладки текущим пользователем
        is_bookmarked = False
        if self.request.user.is_authenticated:
            is_bookmarked = Bookmark.objects.filter(user=self.request.user, movie=movie).exists()
        context["is_bookmarked"] = is_bookmarked

        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        movie = self.get_object()
        bookmark_action = request.POST.get('bookmark_action')

        if bookmark_action == 'add':
            Bookmark.objects.get_or_create(user=request.user, movie=movie)
        elif bookmark_action == 'remove':
            Bookmark.objects.filter(user=request.user, movie=movie).delete()

        return redirect('homepage:detail', pk=movie.pk)
    

@method_decorator(login_required, name='dispatch')
class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def post(self, request):
        form = RatingForm(request.POST)

        if form.is_valid():
            user = request.user 
            Rating.objects.update_or_create(
                user=user,
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
                )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


def all_movie(request): 
    template_name = 'homepage/all_movies.html'
    genre_id = request.GET.get('genre')
    movies_list = VideoProduct.objects.filter(moderated=True).order_by('release_year')

    if genre_id:
        movies_list = movies_list.filter(product_type__id=genre_id)

    context = {
        'object_list': movies_list,
        'form': GenreButtonForm(request.GET or None)
    }
    return render(request, template_name, context)


def genres(request, genre):
    template_name = 'homepage/genre.html'
    movies_list = VideoProduct.objects.filter(product_type__title=genre, moderated=True).order_by('-created_at')
    context = {
        'movies': movies_list,
        'genres': genre
    }
    return render(request, template_name, context)


def years(request, year):
    template_name = 'homepage/year.html'
    movies_list = VideoProduct.objects.filter(release_year__year=year, moderated=True).order_by('-created_at')
    context = {
        'movies': movies_list,
        'years': year
    }
    return render(request, template_name, context)

def random_movie(request):
    template_name = 'homepage/random_movie.html'
    form = GenreForm(request.GET or None)
    random_movie = None

    if form.is_valid():
        genre = form.cleaned_data['genre']
        movies = VideoProduct.objects.filter(product_type__title=genre, moderated=True)
        if movies.exists():
            random_movie = random.choice(movies)
    context = {
            'form': form,
            'random_movie': random_movie
            }
    return render(request, template_name, context)

@staff_member_required
@login_required
def add_movie(request):
    form_class = VideoProductForm
    template_name = 'homepage/add_movie.html'

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = form_class()
    context = {
		'form': form,
	}
    return render(request, template_name, context)

@login_required
def bookmarked_movies(request):
    user_bookmarks = Bookmark.objects.filter(user=request.user)

    movie_list = VideoProduct.objects.filter(moderated=True).order_by('-created_at')
    page_obj_movies = movie_list

    for movie in page_obj_movies:
        if request.user.is_authenticated:
            movie.user_rating = Rating.objects.filter(movie=movie, user=request.user).first()
        else:
            movie.user_rating = None

    context = {
        'user_bookmarks': user_bookmarks,
        'page_obj_movies': page_obj_movies,
    }
    return render(request, 'cinema/videobookmarked_list.html', context)