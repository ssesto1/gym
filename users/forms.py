from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# 1. FORMA ZA REGISTRACIJU
class RegistracijaForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

# 2. FORMA ZA PRIJAVU (Nedostajala je ova klasa!)
class PrijavaForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'premium-input'

# 3. FORMA ZA UREĐIVANJE PROFILA
class ProfilFitnessForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'spol', 'godine', 'tezina', 'visina', 'razina_aktivnosti', 'cilj', 'profilna_slika']
        labels = {
            'first_name': 'Ime',
            'last_name': 'Prezime',
            'spol': 'Spol',
            'godine': 'Godine',
            'tezina': 'Težina (kg)',
            'visina': 'Visina (cm)',
            'razina_aktivnosti': 'Razina aktivnosti',
            'cilj': 'Tvoj cilj',
            'profilna_slika': 'Profilna slika'
        }
        widgets = {
            # Ovo rješava onaj ružni "Currently:" tekst kod slike
            'profilna_slika': forms.FileInput(),
        }