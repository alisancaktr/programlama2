from django.contrib import admin
from django.urls import path
from ana_sayfa.views import login_view, logout_view, dashboard_view, filmler_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('filmler/', filmler_view, name='filmler'),
]