from django.db import models

class Dizi(models.Model):
    baslik = models.CharField(max_length=200)
    tur = models.CharField(max_length=100, blank=True, null=True)
    sezon_sayisi = models.IntegerField(default=1, blank=True, null=True)
    bolum_sayisi = models.IntegerField(default=0, blank=True, null=True)
    puan = models.FloatField(default=0.0, blank=True, null=True)
    afis = models.ImageField(upload_to='dizi_afisler/', blank=True, null=True)
    aciklama = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.baslik