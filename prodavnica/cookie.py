import json
from .models import *

def cookieKorpa(request):
    try:
        korpa = json.loads(request.COOKIES['korpa'])
    except:
        korpa = {}    


    print('Korpa:', korpa)
    kartica = []
    narudzbina = {'ukupno_korpa':0, 'proizvodi_korpa':0, 'dostava':False}
    proizvodiKorpa = narudzbina['proizvodi_korpa']

    for i in korpa:
        try:
            proizvodiKorpa += korpa[i]['kolicina']

            proizvod = Proizvod.objects.get(id=i)
            ukupno = (proizvod.cena * korpa[i]['kolicina'])

            narudzbina['ukupno_korpa'] += ukupno
            narudzbina['proizvodi_korpa'] += ukupno

            kartice = {
                'proizvod':{
                    'id':proizvod.id,
                    'ime':proizvod.ime,
                    'cena':proizvod.cena,
                    'slikaURL':proizvod.slikaURL,
                },
                'kolicina':korpa[i]['kolicina'],
                'ukupna_cena':ukupno,
                }
            kartica.append(kartice)

            if proizvod.digital == False:
                narudzbina['dostava'] = True
        except:
            pass

    return {'proizvodiKorpa': proizvodiKorpa, 'narudzbina': narudzbina, 'kartica': kartica}

