from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import ArkadashlikIstegi


@login_required(login_url='login')
def kullanici_ara_view(request):
    """Kullanıcı arama sayfası"""
    query = request.GET.get('q', '').strip()
    sonuclar = []

    if query:
        sonuclar = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)

    # Her kullanıcı için arkadaşlık durumunu belirle
    sonuclar_durum = []
    for kullanici in sonuclar:
        # Gönderilmiş istek var mı?
        gonderilen = ArkadashlikIstegi.objects.filter(
            gonderen=request.user, alici=kullanici
        ).first()
        # Alınmış istek var mı?
        alinan = ArkadashlikIstegi.objects.filter(
            gonderen=kullanici, alici=request.user
        ).first()

        if gonderilen and gonderilen.durum == 'kabul_edildi':
            durum = 'arkadas'
        elif gonderilen and gonderilen.durum == 'beklemede':
            durum = 'istek_gonderildi'
        elif alinan and alinan.durum == 'beklemede':
            durum = 'istek_alindi'
            durum_obj = alinan
        else:
            durum = 'yabanci'

        sonuclar_durum.append({
            'kullanici': kullanici,
            'durum': durum,
            'istek': gonderilen or alinan,
        })

    return render(request, 'sosyal/kullanici_ara.html', {
        'query': query,
        'sonuclar': sonuclar_durum,
    })


@login_required(login_url='login')
def arkadas_istegi_gonder_view(request, kullanici_id):
    """Arkadaşlık isteği gönder"""
    alici = get_object_or_404(User, id=kullanici_id)

    if alici != request.user:
        # Zaten bir istek varsa tekrar oluşturma
        varmi = ArkadashlikIstegi.objects.filter(
            gonderen=request.user, alici=alici
        ).exists()
        if not varmi:
            ArkadashlikIstegi.objects.create(
                gonderen=request.user,
                alici=alici
            )

    return redirect('kullanici_ara')


@login_required(login_url='login')
def istek_kabul_view(request, istek_id):
    """Arkadaşlık isteğini kabul et"""
    istek = get_object_or_404(ArkadashlikIstegi, id=istek_id, alici=request.user)
    istek.durum = 'kabul_edildi'
    istek.save()
    return redirect('arkadas_istekleri')


@login_required(login_url='login')
def istek_reddet_view(request, istek_id):
    """Arkadaşlık isteğini reddet"""
    istek = get_object_or_404(ArkadashlikIstegi, id=istek_id, alici=request.user)
    istek.durum = 'reddedildi'
    istek.save()
    return redirect('arkadas_istekleri')


@login_required(login_url='login')
def arkadas_istekleri_view(request):
    """Gelen arkadaşlık istekleri"""
    bekleyen_istekler = ArkadashlikIstegi.objects.filter(
        alici=request.user,
        durum='beklemede'
    ).order_by('-tarih')

    arkadaslar = ArkadashlikIstegi.objects.filter(
        Q(gonderen=request.user) | Q(alici=request.user),
        durum='kabul_edildi'
    )

    return render(request, 'sosyal/arkadas_istekleri.html', {
        'bekleyen_istekler': bekleyen_istekler,
        'arkadaslar': arkadaslar,
    })


@login_required(login_url='login')
def profil_view(request, kullanici_id):
    """Bir kullanıcının public profili - film/dizi/kitap yorumları görünür"""
    profil_sahibi = get_object_or_404(User, id=kullanici_id)

    from movies.models import FilmYorum
    from series.models import DiziYorum
    from books.models import KitapYorum

    film_yorumlari = FilmYorum.objects.filter(user=profil_sahibi).select_related('film').order_by('-tarih')[:10]
    dizi_yorumlari = DiziYorum.objects.filter(user=profil_sahibi).select_related('dizi').order_by('-tarih')[:10]
    kitap_yorumlari = KitapYorum.objects.filter(user=profil_sahibi).select_related('kitap').order_by('-tarih')[:10]

    # Arkadaşlık durumu
    iliski = None
    if request.user != profil_sahibi:
        iliski = ArkadashlikIstegi.objects.filter(
            Q(gonderen=request.user, alici=profil_sahibi) |
            Q(gonderen=profil_sahibi, alici=request.user)
        ).first()

    return render(request, 'sosyal/profil.html', {
        'profil_sahibi': profil_sahibi,
        'film_yorumlari': film_yorumlari,
        'dizi_yorumlari': dizi_yorumlari,
        'kitap_yorumlari': kitap_yorumlari,
        'iliski': iliski,
    })
