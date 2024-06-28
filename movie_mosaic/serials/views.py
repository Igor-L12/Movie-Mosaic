from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from serials.models import *
from serials.forms import *
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


class PostDetailView(DetailView):
    model = SerialProduct
    queryset = SerialProduct.objects.filter()
    template_name = 'serials/post_detail.html'
    context_object_name = 'serial'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        serial = self.get_object()
        actors = serial.actors.all()
        actor_names = [actor.full_name for actor in actors]
        context['actors'] = actor_names

        # Получаем рейтинг пользователя для этого фильма
        user_rating = None
        if self.request.user.is_authenticated:
            user_rating_obj = RatingSerial.objects.filter(user=self.request.user, serial=serial).first()
            if user_rating_obj:
                user_rating = user_rating_obj.star.value
        
        context["user_rating"] = user_rating
        context["star_form"] = RatingForm()

    
        is_bookmarked = False
        if self.request.user.is_authenticated:
            is_bookmarked = Bookmark.objects.filter(user=self.request.user, serial=serial).exists()
        context["is_bookmarked"] = is_bookmarked

        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        serial = self.get_object()
        bookmark_action = request.POST.get('bookmark_action')

        if bookmark_action == 'add':
            Bookmark.objects.get_or_create(user=request.user, serial=serial)
        elif bookmark_action == 'remove':
            Bookmark.objects.filter(user=request.user, serial=serial).delete()

        return redirect('serials:detail', pk=serial.pk)
    

class AddStarRating(View):
    """Добавление рейтинга сериалу"""

    def post(self, request):
        form = RatingForm(request.POST)

        if form.is_valid():
            user = request.user 
            RatingSerial.objects.update_or_create(
                user=user,
                serial_id=int(request.POST.get("serial")),
                defaults={'star_id': int(request.POST.get("star"))}
                )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


def all_serials(request): 
    template_name = 'serials/all_serials.html'
    genre_id = request.GET.get('genre')
    serials_list = SerialProduct.objects.filter(moderated=True).order_by('release_year')

    if genre_id:
        serials_list = serials_list.filter(product_type__id=genre_id)

    context = {
        'object_list': serials_list,
        'form': GenreButtonForm(request.GET or None)
    }
    return render(request, template_name, context)


def genres(request, genre):
    template_name = 'serials/genre.html'
    serials_list = SerialProduct.objects.filter(product_type__title=genre, moderated=True).order_by('-created_at')
    context = {
        'serials': serials_list,
        'genres': genre
    }
    return render(request, template_name, context)


def years(request, year):
    template_name = 'serials/year.html'
    serials_list = SerialProduct.objects.filter(release_year__year=year, moderated=True).order_by('-created_at')
    context = {
        'serials': serials_list,
        'years': year
    }
    return render(request, template_name, context)


@login_required
def bookmarked_serials(request):
    user_bookmarks = Bookmark.objects.filter(user=request.user)

    serial_list = SerialProduct.objects.filter(moderated=True).order_by('-created_at')
    page_obj_serials = serial_list

    for serial in page_obj_serials:
        if request.user.is_authenticated:
            serial.user_rating = RatingSerial.objects.filter(serial=serial, user=request.user).first()
        else:
            serial.user_rating = None

    context = {
        'user_bookmarks': user_bookmarks,
        'page_obj_serials': page_obj_serials,
    }
    return render(request, 'serials/serialbookmarked_list.html', context)
