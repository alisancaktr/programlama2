from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import FilmForm

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated and request.method == 'GET':
        return redirect('dashboard')

    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        
        if u: 
            if User.objects.filter(username=u).exists():
                messages.error(request, f"'{u}' ismi kapılmış, başka bir tane dene.")
            elif User.objects.filter(email=e).exists():
                messages.error(request, "Bu e-posta adresiyle daha önce kayıt olunmuş.")
            else:
                try:
                    new_user = User.objects.create_user(username=u, email=e, password=p)
                    login(request, new_user)
                    messages.success(request, f"Hoş geldin {u}! Kaydın başarıyla yapıldı.")
                    return redirect('dashboard')
                except Exception as err:
                    messages.error(request, f"Sistemsel hata: {err}")
        
        elif e and p:
            user_obj = User.objects.filter(email=e).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=p)
                if user:
                    login(request, user)
                    return redirect('dashboard')
            messages.error(request, "Giriş başarısız. E-posta veya şifre yanlış.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')

def filmler_view(request):
    return render(request, 'filmler.html')

def diziler_view(request):
    return render(request, 'diziler.html')

def kitaplar_view(request):
    return render(request, 'kitaplar.html')

def film_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == "POST":
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('filmler')
    else:
        form = FilmForm()
    
    return render(request, 'film_ekle.html', {'form': form})

def dizi_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # İleride buraya dizi kaydetme mantığı gelecek
    return render(request, 'dizi_ekle.html')

def kitap_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # İleride buraya kitap kaydetme mantığı gelecek
    return render(request, 'kitap_ekle.html')