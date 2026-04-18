from django.urls import path
from . import views

urlpatterns = [
    path('', views.filmler_view, name='filmler'),
    path('film-ekle/', views.film_ekle_view, name='film_ekle'),
]