from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Kitap, KitapYorum

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

@login_required(login_url='login')
def kitap_ekle_view(request):
    if request.method == "POST":
        baslik = request.POST.get('baslik', '').strip()

        # DÜZELTME: başlık boşsa kaydetme, forma geri dön
        if not baslik:
            kitaplar = Kitap.objects.filter(user=request.user)
            context = {
                'okumak_istediklerim': kitaplar.filter(liste_durumu='okumak_istediklerim'),
                'okuduklarim': kitaplar.filter(liste_durumu='okuduklarim'),
                'open_modal': True,
                'hata': 'Kitap başlığı zorunludur.'
            }
            return render(request, 'kitaplar.html', context)

        afis_url = request.POST.get('afis_url', '').strip()
        puan = request.POST.get('puan')
        yazar = request.POST.get('yazar', '').strip()
        sayfa_sayisi = request.POST.get('sayfa_sayisi', '')
        basim_yili = request.POST.get('basim_yili', '').strip()
        ozet = request.POST.get('ozet', '').strip()
        liste_durumu = request.POST.get('liste_durumu', 'okumak_istediklerim')

        try:
            puan_val = float(puan) if puan and puan != 'None' else 0.0
        except (ValueError, TypeError):
            puan_val = 0.0

        try:
            sayfa_val = int(sayfa_sayisi) if sayfa_sayisi and sayfa_sayisi.isdigit() else None
        except (ValueError, TypeError):
            sayfa_val = None

        Kitap.objects.create(
            user=request.user,
            baslik=baslik,
            afis_url=afis_url,
            puan=puan_val,
            yazar=yazar,
            sayfa_sayisi=sayfa_val,
            basim_yili=basim_yili,
            ozet=ozet,
            liste_durumu=liste_durumu
        )
        return redirect('kitaplar')

    kitaplar = Kitap.objects.filter(user=request.user)
    context = {
        'okumak_istediklerim': kitaplar.filter(liste_durumu='okumak_istediklerim'),
        'okuduklarim': kitaplar.filter(liste_durumu='okuduklarim'),
        'open_modal': True
    }
    return render(request, 'kitaplar.html', context)

@login_required(login_url='login')
def kitap_detay_view(request, kitap_id):
    kitap = get_object_or_404(Kitap, id=kitap_id)
    if request.method == "POST":
        icerik = request.POST.get('icerik', '').strip()
        puan = request.POST.get('kisisel_puan', 5)
        if icerik:
            KitapYorum.objects.create(
                kitap=kitap,
                user=request.user,
                icerik=icerik,
                kisisel_puan=puan
            )
            return redirect('kitap_detay', kitap_id=kitap.id)

    yorumlar = kitap.yorumlar.all().order_by('-tarih')
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
    kitap = get_object_or_404(Kitap, id=kitap_id, user=request.user)
    if request.method == "POST":
        kitap.delete()
    return redirect('kitaplar')
