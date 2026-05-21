from django.db import models
from django.conf import settings

class Program(models.Model):
    naziv = models.CharField(max_length=100)
    opis = models.TextField(blank=True, null=True)
    kreator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='moji_programi')
    def __str__(self): return self.naziv

class DanTreninga(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='dani')
    naziv = models.CharField(max_length=100)
    def __str__(self): return f"{self.program.naziv} - {self.naziv}"

class Vjezba(models.Model):
    dan = models.ForeignKey(DanTreninga, on_delete=models.CASCADE, related_name='vjezbe')
    redni_broj = models.PositiveIntegerField()
    naziv = models.CharField(max_length=100)
    video = models.FileField(upload_to='vjezbe_videi/', blank=True, null=True, help_text="Kratki MP4 video (do 10 sekundi, max 5MB)")
    class Meta: ordering = ['redni_broj']
    def __str__(self): return f"{self.redni_broj}. {self.naziv}"

class TreningSesija(models.Model):
    korisnik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dan_treninga = models.ForeignKey(DanTreninga, on_delete=models.CASCADE)
    pocetak = models.DateTimeField(auto_now_add=True)
    kraj = models.DateTimeField(null=True, blank=True)
    zavrseno = models.BooleanField(default=False)
    def ukupni_volumen(self): return sum(serija.tezina * serija.ponavljanja for serija in self.serije.all())
    def trajanje(self): return (self.kraj - self.pocetak) if self.kraj else None
    def formatirano_trajanje(self):
        t = self.trajanje()
        return f"{int(t.total_seconds() // 60)} min" if t else "U tijeku"
    def dan_u_tjednu(self):
        dani = ['Ponedjeljak', 'Utorak', 'Srijeda', 'Četvrtak', 'Petak', 'Subota', 'Nedjelja']
        return dani[self.pocetak.weekday()]
    def __str__(self): return f"{self.korisnik.username} - {self.dan_treninga.naziv}"

class OdradenaSerija(models.Model):
    sesija = models.ForeignKey(TreningSesija, on_delete=models.CASCADE, related_name='serije')
    vjezba = models.ForeignKey(Vjezba, on_delete=models.CASCADE)
    broj_serije = models.PositiveIntegerField()
    tezina = models.DecimalField(max_digits=5, decimal_places=2)
    ponavljanja = models.PositiveIntegerField()
    rpe = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    je_pr = models.BooleanField(default=False)
    class Meta: ordering = ['broj_serije']

class KatalogVjezbi(models.Model):
    KATEGORIJE = [
        ('Prsa', 'Prsa'), ('Leđa', 'Leđa'), ('Noge', 'Noge'),
        ('Ramena', 'Ramena'), ('Ruke', 'Ruke'), ('Core', 'Core'), ('Cardio', 'Cardio'),
    ]
    naziv = models.CharField(max_length=100)
    kategorija = models.CharField(max_length=50, choices=KATEGORIJE, default='Prsa')
    video = models.FileField(upload_to='vjezbe_videi/', blank=True, null=True)
    class Meta:
        verbose_name_plural = "Katalog Vježbi"
        ordering = ['kategorija', 'naziv']
    def __str__(self): return f"[{self.kategorija}] {self.naziv}"