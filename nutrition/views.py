from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PlanIshrane, Obrok
import random

def generiraj_plan_logika(user):
    """ Pozadinska funkcija za točan izračun TDEE-a i makronutrijenata """
    tezina = getattr(user, 'tezina', None)
    if not tezina: 
        return None

    visina = getattr(user, 'visina', 180)
    godine = getattr(user, 'godine', 30)
    spol = getattr(user, 'spol', 'M')
    cilj = getattr(user, 'cilj', 'maintain')
    aktivnost = getattr(user, 'razina_aktivnosti', 'umjereno')

    # Mifflin-St Jeor formula
    if spol == 'M':
        bmr = (10 * float(tezina)) + (6.25 * float(visina)) - (5 * godine) + 5
    else:
        bmr = (10 * float(tezina)) + (6.25 * float(visina)) - (5 * godine) - 161

    mnozi = 1.2
    if aktivnost == 'umjereno': 
        mnozi = 1.375
    elif aktivnost == 'aktivan': 
        mnozi = 1.55

    tdee = bmr * mnozi

    # Točno usklađivanje s opcijama iz modela
    if cilj == 'loss': 
        tdee -= 500
    elif cilj == 'bulk': 
        tdee += 500

    ciljne_kalorije = int(tdee)
    ciljni_proteini = int(float(tezina) * 2.0)
    ciljne_masti = int((ciljne_kalorije * 0.25) / 9)
    ciljni_ugljikohidrati = int((ciljne_kalorije - (ciljni_proteini * 4) - (ciljne_masti * 9)) / 4)

    plan, created = PlanIshrane.objects.get_or_create(korisnik=user)
    plan.ciljne_kalorije = ciljne_kalorije
    plan.ciljni_proteini = ciljni_proteini
    plan.ciljni_ugljikohidrati = ciljni_ugljikohidrati
    plan.ciljne_masti = ciljne_masti
    plan.save()
    
    return plan


@login_required(login_url='/korisnici/prijava/')
def moj_plan(request):
    user = request.user
    
    # 1. AKO KORISNIK NEMA TEŽINU, NEMA NI PLANA.
    tezina = getattr(user, 'tezina', None)
    if not tezina:
        return render(request, 'nutrition/moj_plan.html', {'plan': None, 'is_pro_user': getattr(user, 'is_pro', False)})

    plan = getattr(user, 'planishrane', None)
    
    # 2. AKO PLAN NE POSTOJI, GENERIRAJ GA U POZADINI
    if not plan:
        plan = generiraj_plan_logika(user)

    # 3. RUČNO AŽURIRANJE MAKROSA OD STRANE KORISNIKA
    if request.method == 'POST' and plan:
        plan.ciljne_kalorije = request.POST.get('kalorije', plan.ciljne_kalorije)
        plan.ciljni_proteini = request.POST.get('proteini', plan.ciljni_proteini)
        plan.ciljni_ugljikohidrati = request.POST.get('ugljikohidrati', plan.ciljni_ugljikohidrati)
        plan.ciljne_masti = request.POST.get('masti', plan.ciljne_masti)
        plan.save()
        return redirect('nutrition:moj_plan')

    is_pro_user = getattr(user, 'is_pro', False)
    
    return render(request, 'nutrition/moj_plan.html', {
        'plan': plan,
        'is_pro_user': is_pro_user,
    })

@login_required(login_url='/korisnici/prijava/')
def generiraj_plan(request):
    """ Dodjeljuje nasumične obroke iz baze u korisnikov plan """
    user = request.user
    plan = getattr(user, 'planishrane', None)
    
    if not plan:
        plan = generiraj_plan_logika(user)
        if not plan:
            return redirect('users:profil')

    # Brišemo stare obroke iz plana
    plan.obroci.clear()
    
    # Nasumično biramo po jedan obrok iz svake kategorije (ako postoje u bazi)
    doruckovi = list(Obrok.objects.filter(kategorija='Doručak'))
    ruckovi = list(Obrok.objects.filter(kategorija='Ručak'))
    vecere = list(Obrok.objects.filter(kategorija='Večera'))
    snackovi = list(Obrok.objects.filter(kategorija='Međuobrok'))

    if doruckovi: plan.obroci.add(random.choice(doruckovi))
    if ruckovi: plan.obroci.add(random.choice(ruckovi))
    if vecere: plan.obroci.add(random.choice(vecere))
    if snackovi: plan.obroci.add(random.choice(snackovi))

    return redirect('nutrition:moj_plan')
