from django.urls import path
from . import views

urlpatterns = [
    path('', views.diziler_view, name='diziler'), # Başına views. ekledik
    path('dizi-ekle/', views.dizi_ekle_view, name='dizi_ekle'), # Başına views. ekledik
    path('<int:dizi_id>/', views.dizi_detay_view, name='dizi_detay'),
    path('sil/<int:dizi_id>/', views.dizi_sil_view, name='dizi_sil'),
]