from django.db import models
from django.contrib.auth.models import User


class ArkadashlikIstegi(models.Model):
    DURUM_CHOICES = [
        ('beklemede', 'Beklemede'),
        ('kabul_edildi', 'Kabul Edildi'),
        ('reddedildi', 'Reddedildi'),
    ]

    gonderen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gonderilen_istekler')
    alici = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alinan_istekler')
    durum = models.CharField(max_length=20, choices=DURUM_CHOICES, default='beklemede')
    tarih = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('gonderen', 'alici')

    def __str__(self):
        return f"{self.gonderen.username} → {self.alici.username} ({self.durum})"
