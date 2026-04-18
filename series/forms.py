from django import forms
from .models import Dizi

class DiziForm(forms.ModelForm):
    class Meta:
        model = Dizi
        fields = ['baslik', 'tur', 'sezon_sayisi'] # Hızlı ekleme için ideal