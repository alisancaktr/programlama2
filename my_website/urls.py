from django.contrib import admin
from django.urls import path, include
from ana_sayfa.views import (
    index_view, login_view, logout_view, dashboard_view,
    diziler_view, dizi_ekle_view # Kitapları buradan sildik!
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('giris/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    
    # Filmler (Zaten böyleydi)
    path('filmler/', include('movies.urls')),
    
    # Kitaplar (YENİ SİSTEM: Tüm kitap işlerini books/urls.py yönetecek)
    path('kitaplar/', include('books.urls')),
    
    # Diziler (Şimdilik burada kalsın, birazdan bunu da ayıracağız)
    path('diziler/', diziler_view, name='diziler'),
    path('dizi-ekle/', dizi_ekle_view, name='dizi_ekle'),
]