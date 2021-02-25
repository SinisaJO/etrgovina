from django.contrib import admin
from .models import *

admin.site.register(Kupac)
admin.site.register(Proizvod)
admin.site.register(Narudzbina)
admin.site.register(NaruceniProizvod)
admin.site.register(Dostava)

