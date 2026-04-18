from django.db import models
from django.contrib.auth.models import User

class Kitap(models.Model):
    DURUM_CHOICES = [
        ('okumak_istediklerim', 'Okumak İstediklerim'),
        ('okuduklarim', 'Okuduklarım'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    baslik = models.CharField(max_length=255)
    afis_url = models.URLField(max_length=500, blank=True, null=True)
    puan = models.FloatField(default=0) # Genel API puanı veya ortalama
    liste_durumu = models.CharField(max_length=50, choices=DURUM_CHOICES, default='okumak_istediklerim')
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)

    # --- YENİ KÜNYE ALANLARI ---
    yazar = models.CharField(max_length=255, blank=True, null=True)
    sayfa_sayisi = models.IntegerField(blank=True, null=True)
    basim_yili = models.CharField(max_length=10, blank=True, null=True)
    ozet = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.baslik

# --- YORUM SİSTEMİ ---
class KitapYorum(models.Model):
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, related_name='yorumlar')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    icerik = models.TextField()
    kisisel_puan = models.IntegerField(default=5) # Kullanıcının kendi verdiği puan (1-10)
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.kitap.baslik} Yorumu"