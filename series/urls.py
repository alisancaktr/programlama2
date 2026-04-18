from django.urls import path
from .views import diziler_view, dizi_ekle_view

urlpatterns = [
    path('', diziler_view, name='diziler'),
    path('dizi-ekle/', dizi_ekle_view, name='dizi_ekle'),
]