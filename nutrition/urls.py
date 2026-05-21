from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('generiraj/', views.generiraj_plan, name='generiraj_plan'),
    path('moj-plan/', views.moj_plan, name='moj_plan'),
]