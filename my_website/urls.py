from django.contrib import admin
from django.urls import path, include
from ana_sayfa.views import (
    index_view, login_view, logout_view, dashboard_view
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('giris/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    
    # Filmler - Tüm işler movies/urls.py içinde
    path('filmler/', include('movies.urls')),
    
    # Kitaplar - Tüm işler books/urls.py içinde
    path('kitaplar/', include('books.urls')),
    
    # Diziler - Tüm işler series/urls.py içinde
    path('diziler/', include('series.urls')),
    path('sosyal/', include('sosyal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)