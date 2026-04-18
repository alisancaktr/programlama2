from django.contrib import admin
from django.urls import path, include
# Tüm view fonksiyonlarını tek bir parantez içinde import edelim
from ana_sayfa.views import (
    index_view, login_view, logout_view, dashboard_view,
    filmler_view, diziler_view, kitaplar_view,
    dizi_ekle_view, kitap_ekle_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('giris/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    
    # Filmleri yeni oluşturduğumuz movies/urls.py'a yönlendiriyoruz
    path('filmler/', include('movies.urls')),
    
    # Diziler
    path('diziler/', diziler_view, name='diziler'),
    path('dizi-ekle/', dizi_ekle_view, name='dizi_ekle'), # BU EKSİKTİ, EKLEDİK
    
    # Kitaplar
    path('kitaplar/', kitaplar_view, name='kitaplar'),
    path('kitap-ekle/', kitap_ekle_view, name='kitap_ekle'),
]