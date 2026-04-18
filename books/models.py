from django.db import models
from django.contrib.auth.models import User

class Kitap(models.Model):
    DURUM_CHOICES = [
        ('okumak_istediklerim', 'Okumak İstediklerim'),
        ('okuduklarim', 'Okuduklarım'),
    ]

    # 'on_ hisse_delete' kısmını 'on_delete' olarak düzelttik
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baslik = models.CharField(max_length=255)
    afis_url = models.URLField(max_length=500, blank=True, null=True)
    puan = models.FloatField(default=0)
    # Karakter sınırını 20'den 50'ye çıkardık ki hata vermesin
    liste_durumu = models.CharField(max_length=50, choices=DURUM_CHOICES, default='okumak_istediklerim')
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik