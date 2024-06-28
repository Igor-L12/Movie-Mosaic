from django.urls import path
from .views import  PostDetailView, AddStarRating, all_serials, genres, years, bookmarked_serials

app_name = 'serials'

urlpatterns = [
    path('serials/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    path('all-serials/', all_serials, name='all_serials'),
    path('genres/<str:genre>/', genres, name='genres'),
    path('years/<int:year>/', years, name='years'),
    path('bookmarked/', bookmarked_serials, name='bookmarked_serials'),
]