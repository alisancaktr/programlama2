from django.urls import path
from .views import kitaplar_view, kitap_ekle_view

urlpatterns = [
    path('', kitaplar_view, name='kitaplar'), # Bu sayede /kitaplar/ deyince liste gelir
    path('kitap-ekle/', kitap_ekle_view, name='kitap_ekle'), # /kitaplar/kitap-ekle/ olur
]