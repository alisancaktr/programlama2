from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')

        if action == 'register':
            if u and p:
                if not User.objects.filter(username=u).exists():
                    User.objects.create_user(username=u, email=e, password=p)
                    messages.success(request, f"Başarılı! {u} kaydedildi. Şimdi giriş yapabilirsin.")
                    return redirect('login')
                else:
                    messages.error(request, "Bu kullanıcı adı zaten alınmış!")
            else:
                messages.error(request, "Kullanıcı adı ve şifre zorunlu.")

        elif action == 'login':
            try:
                user_obj = User.objects.get(email=e)
                user = authenticate(request, username=user_obj.username, password=p)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Şifre hatalı!")
            except User.DoesNotExist:
                messages.error(request, "Bu e-posta ile kayıtlı kullanıcı bulunamadı.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')

def filmler_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'filmler.html')

def diziler_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'diziler.html')

def kitaplar_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'kitaplar.html')

def film_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'film_ekle.html')

def dizi_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dizi_ekle.html')

def kitap_ekle_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'kitap_ekle.html')