from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from .models import Program, DanTreninga, Vjezba, TreningSesija, OdradenaSerija, KatalogVjezbi
from decimal import Decimal
import json
from django.db.models.functions import TruncDate

@login_required(login_url='/korisnici/prijava/')
def dashboard(request):
    user = request.user
    
    zavrseni_treninzi = OdradenaSerija.objects.filter(
        sesija__korisnik=user,
        sesija__zavrseno=True
    ).annotate(
        datum=TruncDate('sesija__kraj')
    ).values_list('datum', flat=True)

    datumi = list(set([d.strftime('%Y-%m-%d') for d in zavrseni_treninzi if d]))
    datumi_json = json.dumps(datumi)

    sve_serije = OdradenaSerija.objects.filter(
        sesija__korisnik=user, 
        sesija__zavrseno=True
    ).select_related('sesija').order_by('-sesija__kraj')
    
    posjeceni_ids = set()
    lista_treninga = []
    
    for serija in sve_serije:
        if serija.sesija.id not in posjeceni_ids:
            posjeceni_ids.add(serija.sesija.id)
            lista_treninga.append(serija.sesija)

    zadnji_trening = lista_treninga[0] if lista_treninga else None

    kontekst = {
        'datumi_json': datumi_json,
        'treninzi': lista_treninga,
        'sesije': lista_treninga,
        'odradene_sesije': lista_treninga,
        'posljednji_treninzi': lista_treninga[:5],
        'zadnja_sesija': zadnji_trening,
        'zadnji_trening': zadnji_trening,
        'is_pro_user': getattr(user, 'is_pro', False)
    }

    return render(request, 'workouts/dashboard.html', kontekst)

@login_required(login_url='/korisnici/prijava/')
def plan_treninga(request):
    programi = Program.objects.filter(kreator__isnull=True) | Program.objects.filter(kreator=request.user)
    for p in programi:
        p.ukupno_dana = p.dani.count()
        p.zavrseno_dana = TreningSesija.objects.filter(korisnik=request.user, dan_treninga__program=p, zavrseno=True).values('dan_treninga').distinct().count()
        p.postotak = int((p.zavrseno_dana / p.ukupno_dana * 100)) if p.ukupno_dana > 0 else 0
    return render(request, 'workouts/plan_treninga.html', {'programi': programi})

@login_required(login_url='/korisnici/prijava/')
def program_detalji(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    dani = program.dani.all()
    
    aktivna_sesija = TreningSesija.objects.filter(korisnik=request.user, dan_treninga__program=program, zavrseno=False).first()
    aktivni_dan_id = aktivna_sesija.dan_treninga.id if aktivna_sesija else None

    return render(request, 'workouts/program_detalji.html', {
        'program': program, 
        'dani': dani, 
        'aktivni_dan_id': aktivni_dan_id
    })

@login_required(login_url='/korisnici/prijava/')
def zapocni_trening(request, dan_id):
    dan = get_object_or_404(DanTreninga, id=dan_id)
    TreningSesija.objects.get_or_create(korisnik=request.user, dan_treninga=dan, zavrseno=False)
    return redirect('workouts:program_detalji', program_id=dan.program.id)

@login_required(login_url='/korisnici/prijava/')
def vjezba_detalji(request, vjezba_id):
    vjezba = get_object_or_404(Vjezba, id=vjezba_id)
    aktivna_sesija = TreningSesija.objects.filter(korisnik=request.user, dan_treninga=vjezba.dan, zavrseno=False).first()
    
    if request.method == 'POST' and aktivna_sesija:
        tezina = request.POST.get('tezina')
        ponavljanja = request.POST.get('ponavljanja')
        broj_serije = request.POST.get('broj_serije')
        rpe_val = request.POST.get('rpe')
        rpe = float(rpe_val) if rpe_val else None
        
        prosli_pr = OdradenaSerija.objects.filter(sesija__korisnik=request.user, vjezba__naziv=vjezba.naziv, je_pr=True).order_by('-tezina').first()
        je_pr = False
        
        if prosli_pr:
            if float(tezina) > float(prosli_pr.tezina) or (float(tezina) == float(prosli_pr.tezina) and int(ponavljanja) > prosli_pr.ponavljanja):
                je_pr = True
                prosli_pr.je_pr = False
                prosli_pr.save()
        else:
            je_pr = True

        OdradenaSerija.objects.create(sesija=aktivna_sesija, vjezba=vjezba, broj_serije=broj_serije, tezina=tezina, ponavljanja=ponavljanja, rpe=rpe, je_pr=je_pr)
        return redirect(reverse('workouts:vjezba_detalji', args=[vjezba.id]) + '?rest=90')

    odradene_serije = OdradenaSerija.objects.filter(sesija=aktivna_sesija, vjezba=vjezba) if aktivna_sesija else []
    iduca_serija = odradene_serije.last().broj_serije + 1 if odradene_serije else 1

    return render(request, 'workouts/vjezba_detalji.html', {
        'vjezba': vjezba, 'aktivna_sesija': aktivna_sesija, 'odradene_serije': odradene_serije, 'iduca_serija': iduca_serija
    })

@login_required(login_url='/korisnici/prijava/')
def zavrsi_dan(request, dan_id):
    # Popravljen bug: .filter().update() zatvara apsolutno sve zaostale sesije za taj dan odjednom
    TreningSesija.objects.filter(
        korisnik=request.user, 
        dan_treninga_id=dan_id, 
        zavrseno=False
    ).update(
        zavrseno=True, 
        kraj=timezone.now()
    )
    return redirect('workouts:dashboard')

@login_required(login_url='/korisnici/prijava/')
def povijest_treninga(request):
    sesije = TreningSesija.objects.filter(korisnik=request.user, zavrseno=True).order_by('-kraj')
    return render(request, 'workouts/povijest.html', {'sesije': sesije})

@login_required(login_url='/korisnici/prijava/')
def kreiraj_program(request):
    if request.method == 'POST':
        naziv = request.POST.get('naziv')
        opis = request.POST.get('opis')
        program = Program.objects.create(naziv=naziv, opis=opis, kreator=request.user)
        return redirect('workouts:program_detalji', program_id=program.id)
    return render(request, 'workouts/kreiraj_program.html')

@login_required(login_url='/korisnici/prijava/')
def dodaj_dan(request, program_id):
    program = get_object_or_404(Program, id=program_id, kreator=request.user)
    if request.method == 'POST':
        naziv = request.POST.get('naziv')
        DanTreninga.objects.create(program=program, naziv=naziv)
        return redirect('workouts:program_detalji', program_id=program.id)
    return render(request, 'workouts/dodaj_dan.html', {'program': program})

@login_required(login_url='/korisnici/prijava/')
def dodaj_vjezbu(request, dan_id):
    dan = get_object_or_404(DanTreninga, id=dan_id, program__kreator=request.user)
    katalog = KatalogVjezbi.objects.all()

    if request.method == 'POST':
        katalog_id = request.POST.get('katalog_id')
        odabrana_vjezba = get_object_or_404(KatalogVjezbi, id=katalog_id)
        zadnja_vjezba = dan.vjezbe.order_by('redni_broj').last()
        redni_broj = zadnja_vjezba.redni_broj + 1 if zadnja_vjezba else 1
        
        # OVDJE JE BIO BUG: Zamijenjeno odabrana_vjezba.video_fajl u odabrana_vjezba.video
        Vjezba.objects.create(dan=dan, redni_broj=redni_broj, naziv=odabrana_vjezba.naziv, video=odabrana_vjezba.video)
        return redirect('workouts:program_detalji', program_id=dan.program.id)
        
    return render(request, 'workouts/dodaj_vjezbu.html', {'dan': dan, 'katalog': katalog})

@login_required(login_url='/korisnici/prijava/')
def obrisi_program(request, program_id):
    program = get_object_or_404(Program, id=program_id, kreator=request.user)
    program.delete()
    return redirect('workouts:plan_treninga')

@login_required(login_url='/korisnici/prijava/')
def vjezba_analitika(request, vjezba_id):
    vjezba = get_object_or_404(Vjezba, id=vjezba_id)
    is_pro_user = getattr(request.user, 'is_pro', False)

    if not is_pro_user:
        return render(request, 'workouts/vjezba_analitika.html', {
            'vjezba': vjezba, 
            'is_locked': True
        })

    sve_serije = OdradenaSerija.objects.filter(
        sesija__korisnik=request.user,
        vjezba__naziv=vjezba.naziv,
        sesija__zavrseno=True
    ).order_by('sesija__kraj')

    labels = []
    one_rm_data = []
    top_weight_data = []
    posjecene_sesije = set()

    for serija in sve_serije:
        sesija_id = serija.sesija.id
        if sesija_id not in posjecene_sesije:
            najjaca = sve_serije.filter(sesija_id=sesija_id).order_by('-tezina').first()
            labels.append(serija.sesija.kraj.strftime('%d.%m.'))
            top_weight_data.append(float(najjaca.tezina))
            
            reps = najjaca.ponavljanja
            if reps > 0:
                one_rm = float(najjaca.tezina) * (36 / (37 - reps))
                one_rm_data.append(round(one_rm, 1))
            posjecene_sesije.add(sesija_id)

    return render(request, 'workouts/vjezba_analitika.html', {
        'vjezba': vjezba,
        'labels': labels,
        'one_rm_data': one_rm_data,
        'top_weight_data': top_weight_data,
        'is_locked': False
    })

@login_required(login_url='/korisnici/prijava/')
def soba_trofeja(request):
    sve_pr_serije = OdradenaSerija.objects.filter(
        sesija__korisnik=request.user,
        je_pr=True,
        sesija__zavrseno=True
    ).order_by('-tezina')

    top_trofeji = {}
    for serija in sve_pr_serije:
        naziv_vjezbe = serija.vjezba.naziv
        if naziv_vjezbe not in top_trofeji:
            top_trofeji[naziv_vjezbe] = serija

    return render(request, 'workouts/soba_trofeja.html', {
        'trofeji': top_trofeji.values()
    })