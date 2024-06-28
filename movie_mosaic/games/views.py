from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from games.models import *
from games.forms import *
from posts.models import *
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random


def games_index(request):
    game_list = GameProduct.objects.filter(moderated=True).order_by('-created_at')
    paginator_games = Paginator(game_list, 7)
    page_number_games = request.GET.get('page_games')
    page_obj_games = paginator_games.get_page(page_number_games)

    for game in page_obj_games:
        if request.user.is_authenticated:
            game.user_rating = RatingGame.objects.filter(game=game, user=request.user).first()
        else:
            game.user_rating = None

    return page_obj_games
    

class PostDetailView(DetailView):
    model = GameProduct
    queryset = GameProduct.objects.filter()
    template_name = 'games/post_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()

        user_rating = None
        if self.request.user.is_authenticated:
            user_rating_obj = RatingGame.objects.filter(user=self.request.user, game=game).first()
            if user_rating_obj:
                user_rating = user_rating_obj.star.value
        
        context["user_rating"] = user_rating
        context["star_form"] = RatingForm()

    
        is_bookmarked = False
        if self.request.user.is_authenticated:
            is_bookmarked = Bookmark.objects.filter(user=self.request.user, game=game).exists()
        context["is_bookmarked"] = is_bookmarked

        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        game = self.get_object()
        bookmark_action = request.POST.get('bookmark_action')

        if bookmark_action == 'add':
            Bookmark.objects.get_or_create(user=request.user, game=game)
        elif bookmark_action == 'remove':
            Bookmark.objects.filter(user=request.user, game=game).delete()

        return redirect('games:detail', pk=game.pk)

class AddStarRating(View):
    """Добавление рейтинга игре"""

    def post(self, request):
        form = RatingForm(request.POST)

        if form.is_valid():
            user = request.user 
            RatingGame.objects.update_or_create(
                user=user,
                game_id=int(request.POST.get("game")),
                defaults={'star_id': int(request.POST.get("star"))}
                )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
        
def all_games(request): 
    template_name = 'games/all_games.html'
    genre_id = request.GET.get('genre')
    games_list = GameProduct.objects.filter(moderated=True).order_by('release_year')

    if genre_id:
        games_list = games_list.filter(product_type__id=genre_id)

    context = {
        'object_list': games_list,
        'form': GenreButtonForm(request.GET or None)
    }
    return render(request, template_name, context)



def genres(request, genre):
    template_name = 'games/genre.html'
    games_list = GameProduct.objects.filter(product_type__title=genre, moderated=True).order_by('-created_at')
    context = {
        'games': games_list,
        'genres': genre
    }
    return render(request, template_name, context)


def years(request, year):
    template_name = 'games/year.html'
    games_list = GameProduct.objects.filter(release_year__year=year, moderated=True).order_by('-created_at')
    context = {
        'games': games_list,
        'years': year
    }
    return render(request, template_name, context)
    

@login_required
def bookmarked_games(request):
    user_bookmarks = Bookmark.objects.filter(user=request.user)

    games_list = GameProduct.objects.filter(moderated=True).order_by('-created_at')
    page_obj_games = games_list

    for game in page_obj_games:
        if request.user.is_authenticated:
            game.user_rating = RatingGame.objects.filter(game=game, user=request.user).first()
        else:
            game.user_rating = None

    context = {
        'user_bookmarks': user_bookmarks,
        'page_obj_games': page_obj_games,
    }
    return render(request, 'games/gamebookmarked_list.html', context)
