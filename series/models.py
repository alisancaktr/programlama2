from django.db import models
from django.contrib.auth.models import User

class Dizi(models.Model):
    LISTE_SECENEKLERI = [
        ('izlediklerim', 'İzlediğim Diziler'),
        ('izlemek_istediklerim', 'İzlemek İstediğim Diziler'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baslik = models.CharField(max_length=200)
    yonetmen = models.CharField(max_length=200, blank=True, null=True, verbose_name="Yaratıcı/Yönetmen")
    tur = models.CharField(max_length=100, blank=True, null=True)
    puan = models.FloatField(default=0.0)
    afis_url = models.URLField(max_length=500, blank=True, null=True)
    ozet = models.TextField(blank=True, null=True)
    basim_yili = models.CharField(max_length=10, blank=True, null=True)
    
    # Dizilere özel alanlar
    sezon_sayisi = models.IntegerField(default=1)
    bolum_sayisi = models.IntegerField(default=0)
    
    liste_durumu = models.CharField(max_length=30, choices=LISTE_SECENEKLERI, default='izlemek_istediklerim')
    eklenme_tarihi = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.baslik

class DiziYorum(models.Model):
    dizi = models.ForeignKey(Dizi, on_delete=models.CASCADE, related_name='yorumlar')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    icerik = models.TextField()
    kisisel_puan = models.IntegerField(default=5)
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.dizi.baslik} Yorumu"