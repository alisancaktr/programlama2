from django.shortcuts import render, redirect, get_object_or_404
from .models import Film, FilmYorum
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def filmler_view(request):
    # Veritabanından verileri çekiyoruz
    izlediklerim = Film.objects.filter(user=request.user, liste_durumu='izlediklerim').order_by('-eklenme_tarihi')
    izlemek_istediklerim = Film.objects.filter(user=request.user, liste_durumu='izlemek_istediklerim').order_by('-eklenme_tarihi')
    
    context = {
        'izlediklerim': izlediklerim,
        'izlemek_istediklerim': izlemek_istediklerim,
    }
    return render(request, 'filmler.html', context)

@login_required(login_url='login')
def film_ekle_view(request):
    if request.method == 'POST':
        # Formdan gelen verileri tek tek çekiyoruz
        baslik = request.POST.get('baslik', '').strip()
        afis_url = request.POST.get('afis_url', '').strip()
        puan = request.POST.get('puan', '0')
        liste_durumu = request.POST.get('liste_durumu', 'izlemek_istediklerim')

        # Terminale ne geldiğini net görelim
        print(f"\n--- YENİ KAYIT DENEMESİ ---")
        print(f"Gelen Başlık: '{baslik}'")
        print(f"Gelen Liste: {liste_durumu}")

        if baslik: # Başlık doluysa içeri gir
            try:
                # Puanı sayıya çevir
                try:
                    puan_val = float(puan)
                except:
                    puan_val = 0.0

                # KAYIT İŞLEMİ
                Film.objects.create(
                    user=request.user,
                    baslik=baslik,
                    afis_url=afis_url,
                    puan=puan_val,
                    liste_durumu=liste_durumu
                )
                print(f"✅ KAYIT BAŞARILI: {baslik}")
                return redirect('filmler') # Yönlendirme yapmalı (302 kodu)

            except Exception as e:
                # Eğer burada bir hata olursa siyah ekranda DEV harflerle yazar
                print(f"❌ VERİTABANI HATASI: {e}")
        else:
            print("⚠️ HATA: Başlık boş olduğu için 'if baslik' içine girilemedi!")

    return render(request, 'film_ekle.html')


@login_required(login_url='login')
def film_detay_view(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    
    if request.method == "POST":
        icerik = request.POST.get('icerik')
        puan = request.POST.get('kisisel_puan')
        
        if icerik:
            FilmYorum.objects.create(
                film=film,
                user=request.user,
                icerik=icerik,
                kisisel_puan=puan
            )
            return redirect('film_detay', film_id=film.id)

    # Kendi kayıtlı filminin yorumları
    yorumlar = film.yorumlar.all().order_by('-tarih')

    # Aynı başlıktaki diğer kullanıcıların filmlerine yapılan yorumlar
    diger_filmler = Film.objects.filter(baslik__iexact=film.baslik).exclude(id=film.id)
    diger_yorumlar = FilmYorum.objects.filter(
        film__in=diger_filmler
    ).exclude(user=request.user).order_by('-tarih')

    return render(request, 'film_detay.html', {
        'film': film,
        'yorumlar': yorumlar,
        'diger_yorumlar': diger_yorumlar,
    })

@login_required(login_url='login')
def film_sil_view(request, film_id):
    film = get_object_or_404(Film, id=film_id, user=request.user)
    if request.method == "POST":
        film.delete()
    return redirect('filmler') # 'filmler' ana sayfa name'i neyse o