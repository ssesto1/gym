from django.db import models
from django.conf import settings
from decimal import Decimal

class Namirnica(models.Model):
    naziv = models.CharField(max_length=100)
    kalorije = models.PositiveIntegerField(default=0, help_text="Kalorije na 100g")
    proteini = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))
    ugljikohidrati = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))
    masti = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))

    class Meta:
        verbose_name_plural = "Namirnice"

    def __str__(self):
        return f"{self.naziv} ({self.kalorije} kcal)"

class Obrok(models.Model):
    KATEGORIJE = [
        ('Doručak', 'Doručak'), ('Ručak', 'Ručak'),
        ('Večera', 'Večera'), ('Međuobrok', 'Međuobrok'),
    ]
    naziv = models.CharField(max_length=200)
    kategorija = models.CharField(max_length=50, choices=KATEGORIJE)
    recept = models.TextField(blank=True, null=True)
    slika = models.ImageField(upload_to='obroci/', blank=True, null=True)

    @property
    def kalorije(self):
        return int(sum((stavka.namirnica.kalorije / 100) * stavka.gramaza for stavka in self.stavke.all()))

    @property
    def proteini(self):
        return round(sum((float(stavka.namirnica.proteini) / 100) * stavka.gramaza for stavka in self.stavke.all()), 1)

    @property
    def ugljikohidrati(self):
        return round(sum((float(stavka.namirnica.ugljikohidrati) / 100) * stavka.gramaza for stavka in self.stavke.all()), 1)

    @property
    def masti(self):
        return round(sum((float(stavka.namirnica.masti) / 100) * stavka.gramaza for stavka in self.stavke.all()), 1)

    class Meta:
        verbose_name_plural = "Obroci"

    def __str__(self):
        return self.naziv

class StavkaObroka(models.Model):
    obrok = models.ForeignKey(Obrok, on_delete=models.CASCADE, related_name='stavke')
    namirnica = models.ForeignKey(Namirnica, on_delete=models.CASCADE)
    gramaza = models.PositiveIntegerField(default=100)

class PlanIshrane(models.Model):
    korisnik = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='planishrane')
    ciljne_kalorije = models.PositiveIntegerField(default=2000)
    ciljni_proteini = models.PositiveIntegerField(default=150)
    ciljni_ugljikohidrati = models.PositiveIntegerField(default=200)
    ciljne_masti = models.PositiveIntegerField(default=70)
    obroci = models.ManyToManyField(Obrok, blank=True)
    broj_generiranja = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Planovi Ishrane"

    def __str__(self):
        return f"Plan za {self.korisnik.username}"