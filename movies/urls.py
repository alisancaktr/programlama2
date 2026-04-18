from django.urls import path
from . import views

urlpatterns = [
    path('', views.filmler_view, name='filmler'),
    path('film-ekle/', views.film_ekle_view, name='film_ekle'),
    path('<int:film_id>/', views.film_detay_view, name='film_detay'),
    path('sil/<int:film_id>/', views.film_sil_view, name='film_sil'),
]