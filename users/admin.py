from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Ovdje govorimo Djangu da na postojeću formu (Ime, Email, Lozinka) 
    # doda i našu novu sekciju s fitness podacima i PRO statusom
    fieldsets = UserAdmin.fieldsets + (
        ('Fitness Podaci i PRO Status', {
            'fields': ('spol', 'godine', 'tezina', 'visina', 'razina_aktivnosti', 'cilj', 'is_pro', 'profilna_slika')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)