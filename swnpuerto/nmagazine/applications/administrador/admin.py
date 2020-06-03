from django.contrib import admin
from .models import Boleta, DetailBoleta, LostMagazine
# Register your models here.

admin.site.register(Boleta)
admin.site.register(DetailBoleta)
admin.site.register(LostMagazine)
