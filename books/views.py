from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Kitap, KitapYorum

# 1. KİTAPLARI LİSTELEME
@login_required(login_url='login')
def kitaplar_view(request):
    kitaplar = Kitap.objects.filter(user=request.user)
    okumak_istediklerim = kitaplar.filter(liste_durumu='okumak_istediklerim')
    okuduklarim = kitaplar.filter(liste_durumu='okuduklarim')
    
    context = {
        'okumak_istediklerim': okumak_istediklerim,
        'okuduklarim': okuduklarim
    }
    return render(request, 'kitaplar.html', context)

# 2. KİTAP EKLEME
@login_required(login_url='login')
def kitap_ekle_view(request):
    if request.method == "POST":
        baslik = request.POST.get('baslik')
        afis_url = request.POST.get('afis_url')
        puan = request.POST.get('puan')
        yazar = request.POST.get('yazar')
        sayfa_sayisi = request.POST.get('sayfa_sayisi')
        basim_yili = request.POST.get('basim_yili')
        ozet = request.POST.get('ozet')
        liste_durumu = request.POST.get('liste_durumu')

        Kitap.objects.create(
            user=request.user,
            baslik=baslik,
            afis_url=afis_url,
            puan=puan if puan and puan != 'None' else 0,
            yazar=yazar,
            sayfa_sayisi=sayfa_sayisi if (sayfa_sayisi and sayfa_sayisi.isdigit()) else 0,
            basim_yili=basim_yili,
            ozet=ozet,
            liste_durumu=liste_durumu
        )
        return redirect('kitaplar')

    return render(request, 'kitap_ekle.html')

# 3. KİTAP DETAY VE YORUM
@login_required(login_url='login')
def kitap_detay_view(request, kitap_id):
    kitap = get_object_or_404(Kitap, id=kitap_id)
    
    if request.method == "POST":
        icerik = request.POST.get('icerik')
        puan = request.POST.get('kisisel_puan')
        
        if icerik:
            KitapYorum.objects.create(
                kitap=kitap,
                user=request.user,
                icerik=icerik,
                kisisel_puan=puan
            )
            return redirect('kitap_detay', kitap_id=kitap.id)

    yorumlar = kitap.yorumlar.all().order_by('-tarih')

    # Aynı başlıktaki diğer kullanıcıların kitaplarına yapılan yorumlar
    diger_kitaplar = Kitap.objects.filter(baslik__iexact=kitap.baslik).exclude(id=kitap.id)
    diger_yorumlar = KitapYorum.objects.filter(
        kitap__in=diger_kitaplar
    ).exclude(user=request.user).order_by('-tarih')

    return render(request, 'kitap_detay.html', {
        'kitap': kitap,
        'yorumlar': yorumlar,
        'diger_yorumlar': diger_yorumlar,
    })

@login_required(login_url='login')
def kitap_sil_view(request, kitap_id):
    # Kitabı bul, eğer kullanıcıya ait değilse 404 döndür (güvenlik)
    kitap = get_object_or_404(Kitap, id=kitap_id, user=request.user)
    
    if request.method == "POST":
        kitap.delete()
        return redirect('kitaplar')
    
    # Eğer yanlışlıkla GET isteği gelirse silme yapma, listeye geri dön
    return redirect('kitaplar')