from django.urls import path
from . import views

urlpatterns = [
    path('', views.prodavnica, name='prodavnica'),
    path('korpa/', views.korpa, name='korpa'),
    path('placanje/', views.placanje, name='placanje'),
    path('opis/<slug>/', views.opis , name='opis'),

    path('registracija/', views.registracija, name='registracija'),
  
    path('proces_narudzbine/', views.procesNarudzbine, name='proces_narudzbine'),
    path('update_proizvod/', views.updateProizvod, name='update_proizvod'),
]