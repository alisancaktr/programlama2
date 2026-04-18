from django.urls import path
from .views import kitaplar_view, kitap_ekle_view, kitap_detay_view, kitap_sil_view # silme view'ını buraya ekledik

urlpatterns = [
    path('', kitaplar_view, name='kitaplar'),
    path('kitap-ekle/', kitap_ekle_view, name='kitap_ekle'),
    
    # Detay Sayfası
    path('<int:kitap_id>/', kitap_detay_view, name='kitap_detay'),
    
    # Silme İşlemi (Yeni)
    path('sil/<int:kitap_id>/', kitap_sil_view, name='kitap_sil'),
]

