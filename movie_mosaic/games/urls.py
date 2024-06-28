from django.urls import path
from .views import games_index, PostDetailView, AddStarRating, all_games, genres, years, bookmarked_games

app_name = 'games'

urlpatterns = [
    path('', games_index, name='index'),
    path('games/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    path('all-games/', all_games, name='all_games'),
    path('genres/<str:genre>/', genres, name='genres'),
    path('years/<int:year>/', years, name='years'),
    path('bookmarked/', bookmarked_games, name='bookmarked_games'),
]