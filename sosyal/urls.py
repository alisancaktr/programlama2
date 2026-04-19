from django.urls import path
from . import views

urlpatterns = [
    path('ara/', views.kullanici_ara_view, name='kullanici_ara'),
    path('istek-gonder/<int:kullanici_id>/', views.arkadas_istegi_gonder_view, name='arkadas_istegi_gonder'),
    path('istek-kabul/<int:istek_id>/', views.istek_kabul_view, name='istek_kabul'),
    path('istek-reddet/<int:istek_id>/', views.istek_reddet_view, name='istek_reddet'),
    path('istekler/', views.arkadas_istekleri_view, name='arkadas_istekleri'),
    path('profil/<int:kullanici_id>/', views.profil_view, name='kullanici_profil'),
]
