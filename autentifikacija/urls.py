from django.urls import path
from . import views



urlpatterns = [
    path('prijava/', views.prijava, name='prijava'),
    path('registracija/', views.registracija, name='registracija'),
    path('odjava/', views.odjava, name='odjava'),

]