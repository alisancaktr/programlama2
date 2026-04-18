from django.db import models

class Kitap(models.Model):
    baslik = models.CharField(max_length=200)
    yazar = models.CharField(max_length=200, blank=True, null=True) # Boş olabilir
    tur = models.CharField(max_length=100, blank=True, null=True)   # Boş olabilir
    sayfa_sayisi = models.IntegerField(default=0, blank=True, null=True)
    ozet = models.TextField(blank=True, null=True)
    kapak_resmi = models.ImageField(upload_to='kitaplar/', blank=True, null=True)

    def __str__(self):
        return f"{self.baslik}"