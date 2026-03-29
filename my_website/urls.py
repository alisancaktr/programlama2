from django.contrib import admin
from django.urls import path
# Buraya film_ekle_view ekledik:
from ana_sayfa.views import (
    login_view, logout_view, dashboard_view, 
    filmler_view, diziler_view, kitaplar_view, film_ekle_view, dizi_ekle_view, kitap_ekle_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('filmler/', filmler_view, name='filmler'),
    path('diziler/', diziler_view, name='diziler'),
    path('kitaplar/', kitaplar_view, name='kitaplar'),
    # Yeni eklenen satır:
    path('film-ekle/', film_ekle_view, name='film_ekle'),
    path('dizi-ekle/', dizi_ekle_view, name='dizi_ekle'),
    path('kitap-ekle/', kitap_ekle_view, name='kitap_ekle'),
]