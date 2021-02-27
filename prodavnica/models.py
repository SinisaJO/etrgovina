from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse



class Kupac(models.Model):
    korisnik = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    ime = models.CharField(max_length=200, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.ime
    
    class Meta:
        verbose_name_plural = 'Kupac'


class Proizvod(models.Model):
    ime = models.CharField(max_length=200)
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    snizena_cena = models.FloatField(blank=True, null=True)
    opis = models.TextField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    slika = models.ImageField(null=True, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.ime

    def get_absolute_url(self):
        return reverse('opis', args=[str(self.slug)])

    @property
    def slikaURL(self):
        try:
            url = self.slika.url 
        except:
            url = ''
        return url
    

    class Meta:
        verbose_name_plural = 'Proizvod'
    


class Narudzbina(models.Model):
    kupac = models.ForeignKey(Kupac, on_delete=models.SET_NULL, null=True, blank=True)
    datum_narudzbine = models.DateTimeField(auto_now_add=True)
    status_narudzbine = models.BooleanField(default=False, null=True, blank=False)
    id_transakcije = models.CharField(max_length=100, null=True)

    @property
    def ukupno_korpa(self):
        naruceniproizvodi = self.naruceniproizvod_set.all()
        ukupno = sum([kartica.ukupna_cena for kartica in naruceniproizvodi])
        return ukupno

    @property
    def proizvodi_korpa(self):
        naruceniproizvodi = self.naruceniproizvod_set.all()
        ukupno = sum([kartica.kolicina for kartica in naruceniproizvodi])
        return ukupno

    @property
    def dostava(self):
        dostava = False
        naruceniproizvodi = self.naruceniproizvod_set.all()
        for i in naruceniproizvodi:
            if i.proizvod.digital == False:
                dostava = True
        return dostava

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name_plural = 'Narudzbina'

class NaruceniProizvod(models.Model):
    proizvod = models.ForeignKey(Proizvod, on_delete=models.SET_NULL, null=True)
    narudzbina = models.ForeignKey(Narudzbina, on_delete=models.SET_NULL, null=True)
    kolicina = models.IntegerField(default=0, null=True, blank=True)
    datum_dodavanja = models.DateTimeField(auto_now_add=True)

    @property
    def ukupna_cena(self):
        ukupno = self.proizvod.cena * self.kolicina
        return ukupno

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'NaruceniProizvod'    
    
class Dostava(models.Model):
    kupac = models.ForeignKey(Kupac, on_delete=models.SET_NULL, null=True)
    narudzbina = models.ForeignKey(Narudzbina, on_delete=models.SET_NULL, null=True)
    adresa = models.CharField(max_length=200, null=False)
    grad = models.CharField(max_length=200, null=False)
    drzava = models.CharField(max_length=200, null=False)
    postanskibroj = models.CharField(max_length=200, null=False)
    datum_dodavanja = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adresa#adresa u admin panelu
    
    class Meta:
        verbose_name_plural = 'Dostava'