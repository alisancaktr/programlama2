from django.shortcuts import render, redirect
from .models import Dizi
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def diziler_view(request):
    diziler = Dizi.objects.filter(user=request.user)
    context = {
        'izlemek_istediklerim': diziler.filter(liste_durumu='izlemek_istediklerim'),
        'izlediklerim': diziler.filter(liste_durumu='izlediklerim')
    }
    return render(request, 'diziler.html', context)

@login_required(login_url='login')
def dizi_ekle_view(request):
    if request.method == 'POST':
        baslik = request.POST.get('baslik')
        afis_url = request.POST.get('afis_url')
        puan = request.POST.get('puan')
        liste_durumu = request.POST.get('liste_durumu')

        if baslik:
            Dizi.objects.create(
                user=request.user,
                baslik=baslik,
                afis_url=afis_url,
                puan=float(puan) if puan and puan != 'undefined' else 0,
                liste_durumu=liste_durumu
            )
            return redirect('diziler')
            
    return render(request, 'dizi_ekle.html')