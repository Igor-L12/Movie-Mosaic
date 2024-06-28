from django.urls import path

from . import views

app_name='homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path('movies/', views.all_movie, name='all_movie'),
    path('movies/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('genres/<str:genre>/', views.genres, name='genre'),
    path('years/<int:year>/', views.years, name='year'),
    path('randoms/', views.random_movie, name='random_movie'),
    path('add_movies/', views.add_movie, name='add_movie'),
    path('bookmarked/', views.bookmarked_movies, name='bookmarked_movie'),
]