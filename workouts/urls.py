from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('planovi/', views.plan_treninga, name='plan_treninga'),
    path('program/<int:program_id>/', views.program_detalji, name='program_detalji'),
    path('dan/<int:dan_id>/zapocni/', views.zapocni_trening, name='zapocni_trening'),
    path('dan/<int:dan_id>/zavrsi/', views.zavrsi_dan, name='zavrsi_dan'),
    path('vjezba/<int:vjezba_id>/', views.vjezba_detalji, name='vjezba_detalji'),
    path('povijest/', views.povijest_treninga, name='povijest_treninga'),
    path('trofeji/', views.soba_trofeja, name='soba_trofeja'),
    
    # NOVO: RUTE ZA CUSTOM WORKOUT BUILDER
    path('program/kreiraj/', views.kreiraj_program, name='kreiraj_program'),
    path('program/<int:program_id>/dodaj_dan/', views.dodaj_dan, name='dodaj_dan'),
    path('dan/<int:dan_id>/dodaj_vjezbu/', views.dodaj_vjezbu, name='dodaj_vjezbu'),
    path('program/<int:program_id>/obrisi/', views.obrisi_program, name='obrisi_program'),

    # ANALITIKA (NOVO)
    path('vjezba/<int:vjezba_id>/analitika/', views.vjezba_analitika, name='vjezba_analitika'),
]