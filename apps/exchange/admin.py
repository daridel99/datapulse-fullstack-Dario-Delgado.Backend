from django.contrib import admin
from .models import TipoCambio


@admin.register(TipoCambio)
class TipoCambioAdmin(admin.ModelAdmin):
    list_display = ("pais", "tasa", "fecha")
    list_filter = ("fecha",)