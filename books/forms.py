from django import forms
from .models import Kitap

class KitapForm(forms.ModelForm):
    class Meta:
        model = Kitap
        fields = ['baslik', 'yazar', 'tur'] # Sadece en gerekli 3 alan görünür