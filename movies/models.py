from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):
    LISTE_SECENEKLERI = [
        ('izlediklerim', 'İzlediğim Filmler'),
        ('izlemek_istediklerim', 'İzlemek İstediğim Filmler'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baslik = models.CharField(max_length=200)
    tur = models.CharField(max_length=100, blank=True, null=True)
    puan = models.FloatField(default=0.0)
    afis_url = models.URLField(max_length=500, blank=True, null=True) # Orijinal afiş linki için
    liste_durumu = models.CharField(max_length=30, choices=LISTE_SECENEKLERI, default='izlemek_istediklerim')
    eklenme_tarihi = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.baslik