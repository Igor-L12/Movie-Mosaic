from django.urls import path

from . import views

app_name='homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.post_detail, name='detail'),
    path('genres/<str:genre>/', views.genres, name='genre'),
    path('years/<int:year>/', views.years, name='year'),
    path('randoms/', views.random_movie, name='random_movie'),
    path('select_movies/', views.select_movie, name='select_movie'),
]