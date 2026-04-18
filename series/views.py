from django.shortcuts import render, redirect
from .models import Dizi
from .forms import DiziForm

def diziler_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    diziler = Dizi.objects.all()
    return render(request, 'diziler.html', {'diziler': diziler})

def dizi_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Dizi verilerini ve afişini yakala
        form = DiziForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('diziler')
    else:
        form = DiziForm()

    return render(request, 'dizi_ekle.html', {'form': form})