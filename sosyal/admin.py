from django.contrib import admin
from .models import ArkadashlikIstegi

@admin.register(ArkadashlikIstegi)
class ArkadashlikIstegiAdmin(admin.ModelAdmin):
    list_display = ('gonderen', 'alici', 'durum', 'tarih')
    list_filter = ('durum',)
