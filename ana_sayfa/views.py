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
    if request.user.is_authenticated:
        return redirect('dashboard')
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
            user_obj = User.objects.filter(email=e).first()
            if user_obj is not None:
                user = authenticate(request, username=user_obj.username, password=p)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Şifre hatalı!")
            else:
                messages.error(request, "Bu e-posta ile kayıtlı kullanıcı bulunamadı.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    from movies.models import Film, FilmYorum
    from series.models import Dizi, DiziYorum
    from books.models import Kitap, KitapYorum
    from sosyal.models import ArkadashlikIstegi
    from django.db.models import Q

    # Kullanıcının gerçek istatistikleri
    film_count = Film.objects.filter(user=request.user, liste_durumu='izlediklerim').count()
    dizi_count = Dizi.objects.filter(user=request.user, liste_durumu='izlediklerim').count()
    kitap_count = Kitap.objects.filter(user=request.user, liste_durumu='okuduklarim').count()

    # İzleme/Okuma Listesinden son eklenenler (Maks 4 adet)
    watchlist_films = Film.objects.filter(user=request.user, liste_durumu='izlemek_istediklerim').order_by('-eklenme_tarihi')[:2]
    watchlist_series = Dizi.objects.filter(user=request.user, liste_durumu='izlemek_istediklerim').order_by('-eklenme_tarihi')[:2]
    watchlist_books = Kitap.objects.filter(user=request.user, liste_durumu='okumak_istediklerim').order_by('-eklenme_tarihi')[:2]

    watchlist = []
    for f in watchlist_films:
        watchlist.append({'type': 'Film', 'baslik': f.baslik, 'yil': f.basim_yili or '', 'icon': '🎬', 'url': f'/filmler/{f.id}/'})
    for s in watchlist_series:
        watchlist.append({'type': 'Dizi', 'baslik': s.baslik, 'yil': s.basim_yili or '', 'icon': '📺', 'url': f'/diziler/{s.id}/'})
    for b in watchlist_books:
        watchlist.append({'type': 'Kitap', 'baslik': b.baslik, 'yil': b.basim_yili or '', 'icon': '📖', 'url': f'/kitaplar/{b.id}/'})
    watchlist = watchlist[:4]

    # Son puanlananlar (Kullanıcının kendi son 3 yorumu/puanı)
    recent_film_reviews = FilmYorum.objects.filter(user=request.user).order_by('-tarih')[:2]
    recent_dizi_reviews = DiziYorum.objects.filter(user=request.user).order_by('-tarih')[:2]
    recent_book_reviews = KitapYorum.objects.filter(user=request.user).order_by('-tarih')[:2]

    recent_reviews = []
    for r in recent_film_reviews:
        recent_reviews.append({'type': 'Film', 'baslik': r.film.baslik, 'puan': r.kisisel_puan, 'icon': '🎬'})
    for r in recent_dizi_reviews:
        recent_reviews.append({'type': 'Dizi', 'baslik': r.dizi.baslik, 'puan': r.kisisel_puan, 'icon': '📺'})
    for r in recent_book_reviews:
        recent_reviews.append({'type': 'Kitap', 'baslik': r.kitap.baslik, 'puan': r.kisisel_puan, 'icon': '📖'})
    recent_reviews = recent_reviews[:3]

    # Arkadaşların aktivite akışı (Son 24 saat veya genel son 5 yorum)
    friends_ids = []
    friendships = ArkadashlikIstegi.objects.filter(
        (Q(gonderen=request.user) | Q(alici=request.user)) & Q(durum='kabul_edildi')
    )
    for f in friendships:
        if f.gonderen == request.user:
            friends_ids.append(f.alici.id)
        else:
            friends_ids.append(f.gonderen.id)

    friend_film_comments = FilmYorum.objects.filter(user_id__in=friends_ids).order_by('-tarih')[:5]
    friend_dizi_comments = DiziYorum.objects.filter(user_id__in=friends_ids).order_by('-tarih')[:5]
    friend_book_comments = KitapYorum.objects.filter(user_id__in=friends_ids).order_by('-tarih')[:5]

    activities = []
    for c in friend_film_comments:
        activities.append({
            'username': c.user.username,
            'action': 'izledi',
            'type_class': 'type-film',
            'type_lbl': 'Film',
            'title': c.film.baslik,
            'year': c.film.basim_yili or '',
            'rating': c.kisisel_puan,
            'review': c.icerik,
            'time': c.tarih,
            'icon': '🎬'
        })
    for c in friend_dizi_comments:
        activities.append({
            'username': c.user.username,
            'action': 'izledi',
            'type_class': 'type-series',
            'type_lbl': 'Dizi',
            'title': c.dizi.baslik,
            'year': c.dizi.basim_yili or '',
            'rating': c.kisisel_puan,
            'review': c.icerik,
            'time': c.tarih,
            'icon': '📺'
        })
    for c in friend_book_comments:
        activities.append({
            'username': c.user.username,
            'action': 'okudu',
            'type_class': 'type-book',
            'type_lbl': 'Kitap',
            'title': c.kitap.baslik,
            'year': c.kitap.basim_yili or '',
            'rating': c.kisisel_puan,
            'review': c.icerik,
            'time': c.tarih,
            'icon': '📖'
        })

    # Eğer arkadaş aktivitesi yoksa platformdaki diğer üyelerin veya kendi son aktivitelerini göster
    if not activities:
        fallback_film = FilmYorum.objects.order_by('-tarih')[:3]
        fallback_dizi = DiziYorum.objects.order_by('-tarih')[:3]
        fallback_book = KitapYorum.objects.order_by('-tarih')[:3]
        for c in fallback_film:
            activities.append({
                'username': c.user.username,
                'action': 'izledi',
                'type_class': 'type-film',
                'type_lbl': 'Film',
                'title': c.film.baslik,
                'year': c.film.basim_yili or '',
                'rating': c.kisisel_puan,
                'review': c.icerik,
                'time': c.tarih,
                'icon': '🎬'
            })
        for c in fallback_dizi:
            activities.append({
                'username': c.user.username,
                'action': 'izledi',
                'type_class': 'type-series',
                'type_lbl': 'Dizi',
                'title': c.dizi.baslik,
                'year': c.dizi.basim_yili or '',
                'rating': c.kisisel_puan,
                'review': c.icerik,
                'time': c.tarih,
                'icon': '📺'
            })
        for c in fallback_book:
            activities.append({
                'username': c.user.username,
                'action': 'okudu',
                'type_class': 'type-book',
                'type_lbl': 'Kitap',
                'title': c.kitap.baslik,
                'year': c.kitap.basim_yili or '',
                'rating': c.kisisel_puan,
                'review': c.icerik,
                'time': c.tarih,
                'icon': '📖'
            })

    activities.sort(key=lambda x: x['time'], reverse=True)
    activities = activities[:5]

    # Popüler İçerikler (En yüksek puanlılar)
    popular_films = Film.objects.order_by('-puan')[:2]
    popular_series = Dizi.objects.order_by('-puan')[:2]
    popular_books = Kitap.objects.order_by('-puan')[:2]

    popular_items = []
    for f in popular_films:
        popular_items.append({'type': 'Film', 'baslik': f.baslik, 'puan': f.puan, 'afis_url': f.afis_url, 'yil': f.basim_yili or '', 'icon': '🎬', 'url': f'/filmler/{f.id}/'})
    for s in popular_series:
        popular_items.append({'type': 'Dizi', 'baslik': s.baslik, 'puan': s.puan, 'afis_url': s.afis_url, 'yil': s.basim_yili or '', 'icon': '📺', 'url': f'/diziler/{s.id}/'})
    for b in popular_books:
        popular_items.append({'type': 'Kitap', 'baslik': b.baslik, 'puan': b.puan, 'afis_url': b.afis_url, 'yil': b.basim_yili or '', 'icon': '📖', 'url': f'/kitaplar/{b.id}/'})
    popular_items.sort(key=lambda x: x['puan'], reverse=True)
    popular_items = popular_items[:5]

    context = {
        'film_count': film_count,
        'dizi_count': dizi_count,
        'kitap_count': kitap_count,
        'watchlist': watchlist,
        'recent_reviews': recent_reviews,
        'activities': activities,
        'popular_items': popular_items,
    }
    return render(request, 'dashboard.html', context)

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