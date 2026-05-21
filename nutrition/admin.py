from django.contrib import admin
from .models import Namirnica, Obrok, StavkaObroka, PlanIshrane

# 1. OPTIMIZIRANI UNOS NAMIRNICA
@admin.register(Namirnica)
class NamirnicaAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'kalorije', 'proteini', 'ugljikohidrati', 'masti')
    search_fields = ('naziv',)  # OVO JE KLJUČNO: Omogućuje pretragu namirnica po imenu
    list_filter = ('kalorije',)
    ordering = ('naziv',)

# 2. INLINE UNOS SA PRETRAGOM
class StavkaObrokaInline(admin.TabularInline):
    model = StavkaObroka
    extra = 1
    autocomplete_fields = ['namirnica']  # Umjesto ogromnog padajućeg menija, sada imaš brzu tražilicu

# 3. ADMIN ZA OBROKE
@admin.register(Obrok)
class ObrokAdmin(admin.ModelAdmin):
    list_display = ('naziv', 'kategorija', 'prikaz_makrosa')
    list_filter = ('kategorija',)
    search_fields = ('naziv',)
    inlines = [StavkaObrokaInline]

    def prikaz_makrosa(self, obj):
        # Brzi uvid u adminu koliko namirnica obrok sadrži
        return f"{obj.stavke.count()} sastojaka"
    prikaz_makrosa.short_description = "Sastav"

# 4. ADMIN ZA PLANOVE
@admin.register(PlanIshrane)
class PlanIshraneAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'ciljne_kalorije', 'ciljni_proteini', 'ciljni_ugljikohidrati', 'ciljne_masti')
    search_fields = ('korisnik__username', 'korisnik__email')
    filter_horizontal = ('obroci',)  # Lijep dizajn s dvije kolone za prebacivanje dodijeljenih obroka