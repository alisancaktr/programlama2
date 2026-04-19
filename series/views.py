from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Dizi, DiziYorum

@login_required(login_url='login')
def diziler_view(request):
    # Tüm dizileri değil, durumuna göre ayrı ayrı filtrelemeliyiz
    izlediklerim = Dizi.objects.filter(
        user=request.user, 
        liste_durumu='izlediklerim' # Models.py'daki key ile aynı olmalı
    )
    
    izlemek_istediklerim = Dizi.objects.filter(
        user=request.user, 
        liste_durumu='izlemek_istediklerim'
    )
    
    context = {
        'izlediklerim': izlediklerim,
        'izlemek_istediklerim': izlemek_istediklerim
    }
    return render(request, 'diziler.html', context)

@login_required(login_url='login')
def dizi_ekle_view(request):
    if request.method == "POST":
        # Formdan gelen 'liste_durumu' verisini çekiyoruz
        liste_durumu = request.POST.get('liste_durumu') 
        
        # Diziyi oluştururken bu durumu açıkça belirtmeliyiz
        Dizi.objects.create(
            user=request.user,
            baslik=request.POST.get('baslik'),
            yonetmen=request.POST.get('yonetmen'),
            tur=request.POST.get('tur'),
            puan=request.POST.get('puan'),
            afis_url=request.POST.get('afis_url'),
            # KRİTİK NOKTA: Buraya dikkat!
            liste_durumu=liste_durumu 
        )
        return redirect('diziler')
    return render(request, 'dizi_ekle.html')

@login_required(login_url='login')
def dizi_detay_view(request, dizi_id):
    dizi = get_object_or_404(Dizi, id=dizi_id)
    
    if request.method == "POST":
        icerik = request.POST.get('icerik')
        puan = request.POST.get('kisisel_puan')
        if icerik:
            DiziYorum.objects.create(
                dizi=dizi, user=request.user, 
                icerik=icerik, kisisel_puan=puan
            )
            return redirect('dizi_detay', dizi_id=dizi.id)

    yorumlar = dizi.yorumlar.all().order_by('-tarih')

    # Aynı başlıktaki diğer kullanıcıların dizilerine yapılan yorumlar
    diger_diziler = Dizi.objects.filter(baslik__iexact=dizi.baslik).exclude(id=dizi.id)
    diger_yorumlar = DiziYorum.objects.filter(
        dizi__in=diger_diziler
    ).exclude(user=request.user).order_by('-tarih')

    return render(request, 'dizi_detay.html', {
        'dizi': dizi,
        'yorumlar': yorumlar,
        'diger_yorumlar': diger_yorumlar,
    })

@login_required(login_url='login')
def dizi_sil_view(request, dizi_id):
    dizi = get_object_or_404(Dizi, id=dizi_id, user=request.user)
    if request.method == "POST":
        dizi.delete()
    return redirect('diziler')