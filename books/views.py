from django.shortcuts import render, redirect
from .models import Kitap
from .forms import KitapForm

def kitaplar_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    kitaplar = Kitap.objects.all()
    return render(request, 'kitaplar.html', {'kitaplar': kitaplar})

def kitap_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Kitap verilerini ve kapak resmini yakala
        form = KitapForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('kitaplar') # Başarılıysa liste sayfasına dön
    else:
        # Sayfa ilk açıldığında boş form gönder
        form = KitapForm()

    return render(request, 'kitap_ekle.html', {'form': form})