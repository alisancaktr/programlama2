from django.shortcuts import render, redirect
from .models import Kitap
from django.contrib.auth.decorators import login_required

# 1. KİTAPLARI LİSTELEME FONKSİYONU
@login_required(login_url='login')
def kitaplar_view(request):
    # Sadece giriş yapmış kullanıcının kitaplarını getir
    kitaplar = Kitap.objects.filter(user=request.user)
    
    # Listeleri ayırmak istersen (Template içinde kullanmak için)
    okumak_istediklerim = kitaplar.filter(liste_durumu='okumak_istediklerim')
    okuduklarim = kitaplar.filter(liste_durumu='okuduklarim')
    
    context = {
        'kitaplar': kitaplar,
        'okumak_istediklerim': okumak_istediklerim,
        'okuduklarim': okuduklarim
    }
    return render(request, 'kitaplar.html', context)

# 2. AKILLI KİTAP EKLEME FONKSİYONU
@login_required(login_url='login')
def kitap_ekle_view(request):
    if request.method == 'POST':
        # Formdan değil, HTML'deki 'name' etiketlerinden verileri çekiyoruz
        baslik = request.POST.get('baslik')
        afis_url = request.POST.get('afis_url')
        puan = request.POST.get('puan')
        liste_durumu = request.POST.get('liste_durumu')

        if baslik:
            # Kitabı veritabanına mühürle
            Kitap.objects.create(
                user=request.user,
                baslik=baslik,
                afis_url=afis_url,
                puan=float(puan) if puan and puan != 'undefined' else 0,
                liste_durumu=liste_durumu
            )
            print(f"✅ KİTAP KAYIT BAŞARILI: {baslik}") # Terminalden takip etmen için
            return redirect('kitaplar')
            
    return render(request, 'kitap_ekle.html')