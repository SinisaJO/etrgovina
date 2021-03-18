from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import DetailView
from django.http import JsonResponse
import json 
import datetime

from .cookie import cookieKorpa


def prodavnica(request):
    if request.user.is_authenticated:
        kupac = request.user.kupac
        narudzbina, otvorena = Narudzbina.objects.get_or_create(kupac=kupac, status_narudzbine=False)
        kartica = narudzbina.naruceniproizvod_set.all()
        proizvodiKorpa = narudzbina.proizvodi_korpa
    else:
        cookieData = cookieKorpa(request)
        proizvodiKorpa = cookieData['proizvodiKorpa']
        
    

    proizvodi = Proizvod.objects.all()
    sadrzaj = {'proizvodi':proizvodi,'proizvodiKorpa': proizvodiKorpa}
    return render(request, 'prodavnica.html', sadrzaj)


def opis(request, slug):
    proizvod = Proizvod.objects.all()
    proizvod = get_object_or_404(proizvod, slug=slug)
    if request.user.is_authenticated:
        kupac = request.user.kupac
        narudzbina, otvorena = Narudzbina.objects.get_or_create(kupac=kupac, status_narudzbine=False)
        proizvodiKorpa = narudzbina.proizvodi_korpa
    else:
        cookieData = cookieKorpa(request)
        proizvodiKorpa = cookieData['proizvodiKorpa']


    
    sadrzaj = {'proizvod': proizvod,'proizvodiKorpa': proizvodiKorpa}
    return render(request, 'opis.html', sadrzaj)

def korpa(request):
    if request.user.is_authenticated:
        kupac = request.user.kupac
        narudzbina, otvorena = Narudzbina.objects.get_or_create(kupac=kupac, status_narudzbine=False)
        kartica = narudzbina.naruceniproizvod_set.all()
        proizvodiKorpa = narudzbina.proizvodi_korpa
    else:
        cookieData = cookieKorpa(request)
        proizvodiKorpa = cookieData['proizvodiKorpa']
        narudzbina = cookieData['narudzbina']
        kartica = cookieData['kartica']

    sadrzaj = {'kartica': kartica, 'narudzbina': narudzbina, 'proizvodiKorpa': proizvodiKorpa}
    return render(request, 'korpa.html', sadrzaj)


def placanje(request):
    if request.user.is_authenticated:
        kupac = request.user.kupac
        narudzbina, otvorena = Narudzbina.objects.get_or_create(kupac=kupac, status_narudzbine=False)
        kartica = narudzbina.naruceniproizvod_set.all()
        proizvodiKorpa = narudzbina.proizvodi_korpa
    else:
        cookieData = cookieKorpa(request)
        proizvodiKorpa = cookieData['proizvodiKorpa']
        narudzbina = cookieData['narudzbina']
        kartica = cookieData['kartica']

    sadrzaj = {'kartica': kartica, 'narudzbina': narudzbina, 'proizvodiKorpa': proizvodiKorpa}
    return render(request, 'placanje.html', sadrzaj)


def updateProizvod(request):
	data = json.loads(request.body)
	proizvodId = data['proizvodId']
	action = data['action']
	print('Action:', action)
	print('Proizvod:', proizvodId)

	kupac = request.user.kupac
	proizvod = Proizvod.objects.get(id=proizvodId)
	narudzbina, otvorena = Narudzbina.objects.get_or_create(kupac=kupac, status_narudzbine=False)

	naruceniProizvod, otvorena = NaruceniProizvod.objects.get_or_create(narudzbina=narudzbina, proizvod=proizvod)

	if action == 'dodaj':
		naruceniProizvod.kolicina = (naruceniProizvod.kolicina + 1)
	elif action == 'oduzmi':
		naruceniProizvod.kolicina = (naruceniProizvod.kolicina - 1)

	naruceniProizvod.save()

	if naruceniProizvod.kolicina <= 0:
		naruceniProizvod.delete()

	return JsonResponse('Proizvod je dodat', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def procesNarudzbine(request):
        id_transakcije = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            kupac = request.user.kupac
            narudzbina, otvorena = Narudzbina.objects.get_or_create(kupac=kupac, status_narudzbine=False)
     
        else:
            print("Korisnik nije prijavljen!")

            print('COOKIES:', request.COOKIES)
            ime = data['form']['ime']
            email = data['form']['email']

            cookieData = cookieKorpa(request)
            kartica = cookieData['kartica']

            kupac, otvorena = Kupac.objects.get_or_create(
                email=email
                )
            kupac.ime = ime
            kupac.save()

            narudzbina = Narudzbina.objects.create(kupac=kupac, status_narudzbine=False,)
            
            for kartice in kartica:
                proizvod = Proizvod.objects.get(id=kartice['proizvod']['id'])

                naruceniProizvod = NaruceniProizvod.objects.create(
                    proizvod=proizvod, narudzbina=narudzbina, kolicina=kartice['kolicina']
                    )

        ukupno = float(data['form']['ukupno'])
        narudzbina.id_transakcije = id_transakcije

        if ukupno == float(narudzbina.ukupno_korpa):
            narudzbina.status_narudzbine = True
        narudzbina.save()
        
        if narudzbina.dostava == True:
            Dostava.objects.create(
                kupac=kupac,
                narudzbina=narudzbina,
                adresa=data['dostava']['adresa'],
                grad=data['dostava']['grad'],
                drzava=data['dostava']['drzava'],
                postanskibroj=data['dostava']['postanskibroj'],
            )

        return JsonResponse('Isplata izvrsena..', safe=False)
