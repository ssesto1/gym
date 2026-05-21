from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('prijava/', views.prijava, name='prijava'),
    path('odjava/', views.odjava, name='odjava'),
    path('registracija/', views.registracija, name='registracija'),
    path('profil/', views.profil, name='profil'),
    path('profil/uredi/', views.uredi_profil, name='uredi_profil'),
]