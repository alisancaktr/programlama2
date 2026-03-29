from django.db import models

class Film(models.Model):
    baslik = models.CharField(max_length=200)
    tur = models.CharField(max_length=100)
    puan = models.FloatField(default=0.0)
    afis = models.ImageField(upload_to='afisler/', blank=True, null=True)
    aciklama = models.TextField(blank=True)

    def __str__(self):
        return self.baslik