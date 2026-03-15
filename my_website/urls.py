from django.contrib import admin
from django.urls import path
from ana_sayfa.views import login_view, logout_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'), # Giriş ekranı
    path('dashboard/', dashboard_view, name='dashboard'), # Ana ekran
    path('logout/', logout_view, name='logout'), # Çıkış işlemi
]