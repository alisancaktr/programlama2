from django.shortcuts import render, redirect
from .models import Film

# Filmleri listelere ayırarak gösteren fonksiyon
def filmler_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Kullanıcının filmlerini 'İzlediklerim' ve 'İzleyeceklerim' olarak ayırıyoruz
    izlediklerim = Film.objects.filter(user=request.user, liste_durumu='izlediklerim').order_by('-eklenme_tarihi')
    izlemek_istediklerim = Film.objects.filter(user=request.user, liste_durumu='izlemek_istediklerim').order_by('-eklenme_tarihi')
    
    context = {
        'izlediklerim': izlediklerim,
        'izlemek_istediklerim': izlemek_istediklerim,
    }
    return render(request, 'filmler.html', context)

# JavaScript'ten gelen verileri veritabanına kaydeden fonksiyon
def film_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Formdan (veya JavaScript'in doldurduğu gizli inputlardan) verileri alıyoruz
        baslik = request.POST.get('baslik')
        afis_url = request.POST.get('afis_url')
        puan = request.POST.get('puan')
        liste_durumu = request.POST.get('liste_durumu')

        # Veritabanına yeni kaydı oluşturuyoruz
        if baslik: # En azından bir başlık seçilmişse kaydet
            Film.objects.create(
                user=request.user,
                baslik=baslik,
                afis_url=afis_url,
                puan=puan if puan else 0.0,
                liste_durumu=liste_durumu
            )
            return redirect('filmler') # Kayıttan sonra listeye dön

    return render(request, 'film_ekle.html')