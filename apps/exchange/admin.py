from django.contrib import admin
from .models import TipoCambio


@admin.register(TipoCambio)
class TipoCambioAdmin(admin.ModelAdmin):
    list_display = ("pais", "tasa", "fecha")
    list_filter = ("pais", "fecha")
    search_fields = ("pais__nombre", "pais__codigo_iso")