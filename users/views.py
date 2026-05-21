from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistracijaForm, PrijavaForm, ProfilFitnessForm
from workouts.models import TreningSesija, OdradenaSerija

def registracija(request):
    if request.user.is_authenticated:
        return redirect('workouts:dashboard')
        
    if request.method == 'POST':
        form = RegistracijaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Uspješna registracija! Dobrodošao.")
            return redirect('users:uredi_profil')
    else:
        form = RegistracijaForm()
    return render(request, 'users/registracija.html', {'form': form})

def prijava(request):
    if request.user.is_authenticated:
        return redirect('workouts:dashboard')
        
    if request.method == 'POST':
        form = PrijavaForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('workouts:dashboard')
    else:
        form = PrijavaForm()
    return render(request, 'users/prijava.html', {'form': form})

def odjava(request):
    logout(request)
    return redirect('users:prijava')

@login_required(login_url='/korisnici/prijava/')
def uredi_profil(request):
    if request.method == 'POST':
        form = ProfilFitnessForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            try:
                from nutrition.views import generiraj_plan_logika
                generiraj_plan_logika(user)
            except Exception as e:
                pass
                
            messages.success(request, "Podaci uspješno ažurirani!")
            return redirect('users:profil')
    else:
        form = ProfilFitnessForm(instance=request.user)
    return render(request, 'users/uredi_profil.html', {'form': form})

@login_required(login_url='/korisnici/prijava/')
def profil(request):
    user = request.user
    
    if request.method == 'POST':
        try:
            # Direktan i siguran upis podataka iz ujednačenog HTML-a
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            
            tezina_raw = request.POST.get('tezina')
            visina_raw = request.POST.get('visina')
            godine_raw = request.POST.get('godine')
            
            if tezina_raw: user.tezina = float(tezina_raw)
            if visina_raw: user.visina = int(visina_raw)
            if godine_raw: user.godine = int(godine_raw)
            
            user.spol = request.POST.get('spol', user.spol)
            user.cilj = request.POST.get('cilj', user.cilj)
            user.save()
            
            # AUTOMATSKO PRERAČUNAVANJE KALORIJA I MAKROSA ODMAH NAKON SPREMANJA
            from nutrition.views import generiraj_plan_logika
            generiraj_plan_logika(user)
            
            messages.success(request, "Profil uspješno ažuriran!")
        except Exception as e:
            messages.error(request, f"Greška pri spremanju: {e}")
            
        return redirect('users:profil')

    # Dohvaćanje podataka za interaktivni grafikon
    sve_serije = OdradenaSerija.objects.filter(
        sesija__korisnik=user,
        sesija__zavrseno=True
    ).select_related('sesija').order_by('sesija__kraj')

    posjecene_sesije = []
    sesija_map = {}

    for serija in sve_serije:
        sid = serija.sesija.id
        if sid not in sesija_map:
            posjecene_sesije.append(serija.sesija)
            t = serija.sesija.trajanje()
            trajanje_min = int(t.total_seconds() // 60) if t else 0
            sesija_map[sid] = {
                'volumen': 0,
                'reps': 0,
                'trajanje': trajanje_min,
                'label': serija.sesija.kraj.strftime('%d.%m.')
            }
        
        sesija_map[sid]['volumen'] += float(serija.tezina) * serija.ponavljanja
        sesija_map[sid]['reps'] += serija.ponavljanja

    labels = [sesija_map[s.id]['label'] for s in posjecene_sesije]
    volumen_po_treningu = [round(sesija_map[s.id]['volumen'], 1) for s in posjecene_sesije]
    ponavljanja_po_treningu = [sesija_map[s.id]['reps'] for s in posjecene_sesije]
    trajanje_po_treningu = [sesija_map[s.id]['trajanje'] for s in posjecene_sesije]

    return render(request, 'users/profil.html', {
        'u': user,
        'labels': labels,
        'volumen_po_treningu': volumen_po_treningu,
        'ponavljanja_po_treningu': ponavljanja_po_treningu,
        'trajanje_po_treningu': trajanje_po_treningu,
    })