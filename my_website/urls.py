from django.contrib import admin
from django.urls import path
<<<<<<< HEAD
from ana_sayfa.views import login_view, logout_view, dashboard_view, filmler_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('filmler/', filmler_view, name='filmler'),
=======
from ana_sayfa.views import login_view, logout_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'), # Giriş ekranı
    path('dashboard/', dashboard_view, name='dashboard'), # Ana ekran
    path('logout/', logout_view, name='logout'), # Çıkış işlemi
>>>>>>> 4cc4eff197454fec2de41425b4e25b5be827bd35
]