from django import forms
from .models import Film

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['baslik', 'tur', 'puan', 'aciklama', 'afis']
        # Kutucukları şıklaştıralım:
        widgets = {
            'baslik': forms.TextInput(attrs={'placeholder': 'Film Adı'}),
            'tur': forms.TextInput(attrs={'placeholder': 'Aksiyon, Dram vb.'}),
            'aciklama': forms.Textarea(attrs={'rows': 3}),
        }
        