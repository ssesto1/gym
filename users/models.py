from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Muško'),
        ('Z', 'Žensko'),
    ]
    
    ACTIVITY_CHOICES = [
        ('neaktivan', 'Neaktivan (bez treninga)'),
        ('umjereno', 'Umjereno aktivan (lagani trening)'),
        ('aktivan', 'Aktivan (redovni trening/kardio)'),
    ]

    GOAL_CHOICES = [
        ('loss', 'Weight loss (mršavljenje)'),
        ('maintain', 'Maintenance (održavanje)'),
        ('bulk', 'Bulk (dobivanje mase)'),
    ]

    # Prilagođena polja specifična za fitness aplikaciju
    spol = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    godine = models.PositiveIntegerField(blank=True, null=True)
    visina = models.PositiveIntegerField(blank=True, null=True, help_text="Visina u cm")
    tezina = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Trenutna težina u kg")
    
    razina_aktivnosti = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, blank=True, null=True)
    cilj = models.CharField(max_length=15, choices=GOAL_CHOICES, blank=True, null=True)
    is_pro = models.BooleanField(default=False)
    profilna_slika = models.ImageField(upload_to='profilne_slike/', default='profilne_slike/default_avatar.png', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"