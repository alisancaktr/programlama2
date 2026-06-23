from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    ad_soyad = models.CharField(max_length=150, blank=True)
    biyografi = models.TextField(max_length=500, blank=True)
    profil_resmi = models.ImageField(upload_to='profil_resimleri/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profili"


# DÜZELTME: Tek bir signal yeterli — profil_kaydet kaldırıldı,
# profil_olustur sadece yeni kullanıcı oluşturulduğunda çalışır.
@receiver(post_save, sender=User)
def profil_olustur_veya_kaydet(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)
    elif hasattr(instance, 'profil'):
        instance.profil.save()
