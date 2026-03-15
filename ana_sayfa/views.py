from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    # Eğer zaten birisi giriş yapmışsa (Ali, Veli vb.) sayfayı açtığında direkt Dashboard'a atar
    if request.user.is_authenticated and request.method == 'GET':
        return redirect('dashboard')

    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        
        # --- KAYIT İŞLEMİ (Eğer kullanıcı adı gelmişse) ---
        if u: 
            if User.objects.filter(username=u).exists():
                messages.error(request, f"'{u}' ismi kapılmış, başka bir tane dene.")
            elif User.objects.filter(email=e).exists():
                messages.error(request, "Bu e-posta adresiyle daha önce kayıt olunmuş.")
            else:
                try:
                    # 1. Kullanıcıyı yarat
                    new_user = User.objects.create_user(username=u, email=e, password=p)
                    # 2. Arda'yı otomatik olarak sisteme dahil et (Login yap)
                    login(request, new_user)
                    messages.success(request, f"Hoş geldin {u}! Kaydın başarıyla yapıldı.")
                    # 3. Bekletmeden Dashboard'a gönder
                    return redirect('dashboard')
                except Exception as err:
                    messages.error(request, f"Sistemsel hata: {err}")
        
        # --- GİRİŞ İŞLEMİ (Eğer kullanıcı adı boş ama email-şifre doluysa) ---
        elif e and p:
            user_obj = User.objects.filter(email=e).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=p)
                if user:
                    login(request, user)
                    return redirect('dashboard')
            
            # Eğer buraya kadar geldiyse giriş hatalıdır
            messages.error(request, "Giriş başarısız. E-posta veya şifre yanlış.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')