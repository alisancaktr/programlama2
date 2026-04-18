from django.db import models
from django.contrib.auth.models import User

class Dizi(models.Model):
    DURUM_CHOICES = [
        ('izlemek_istediklerim', 'İzlemek İstediklerim'),
        ('izlediklerim', 'İzlediklerim'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baslik = models.CharField(max_length=255)
    afis_url = models.URLField(max_length=500, blank=True, null=True)
    puan = models.FloatField(default=0)
    liste_durumu = models.CharField(max_length=50, choices=DURUM_CHOICES, default='izlemek_istediklerim')
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik