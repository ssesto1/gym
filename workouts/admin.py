from django.contrib import admin
from .models import Program, DanTreninga, Vjezba, TreningSesija, OdradenaSerija, KatalogVjezbi

class ProgramAdmin(admin.ModelAdmin):
    list_display = ['naziv', 'kreator']
    list_filter = ['kreator']

class DanTreningaAdmin(admin.ModelAdmin):
    list_display = ['naziv', 'program']
    list_filter = ['program']

class VjezbaAdmin(admin.ModelAdmin):
    list_display = ['redni_broj', 'naziv', 'dan']
    list_filter = ['dan__program', 'dan']
    # Dodana tražilica da lakše nađeš vježbu kad ih bude puno
    search_fields = ['naziv']

class TreningSesijaAdmin(admin.ModelAdmin):
    list_display = ['korisnik', 'dan_treninga', 'pocetak', 'kraj', 'zavrseno']
    list_filter = ['zavrseno', 'korisnik', 'dan_treninga__program']

class OdradenaSerijaAdmin(admin.ModelAdmin):
    list_display = ['sesija', 'vjezba', 'broj_serije', 'tezina', 'ponavljanja', 'je_pr']
    list_filter = ['je_pr']

class KatalogVjezbiAdmin(admin.ModelAdmin):
    # Ovdje smo dodali indikator za video i moćnu tražilicu
    list_display = ['naziv', 'ima_video']
    search_fields = ['naziv']

    def ima_video(self, obj):
        # Provjerava postoji li datoteka u polju video (pod uvjetom da si to polje stavio u model KatalogVjezbi)
        return bool(obj.video)
    
    ima_video.boolean = True
    ima_video.short_description = 'Video učitan'

admin.site.register(Program, ProgramAdmin)
admin.site.register(DanTreninga, DanTreningaAdmin)
admin.site.register(Vjezba, VjezbaAdmin)
admin.site.register(TreningSesija, TreningSesijaAdmin)
admin.site.register(OdradenaSerija, OdradenaSerijaAdmin)
admin.site.register(KatalogVjezbi, KatalogVjezbiAdmin)