from django.db import models
from apps.countries.models import Pais


class TipoCambio(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    moneda_destino = models.CharField(max_length=10, default="USD")
    tasa = models.FloatField()
    fecha = models.DateField()
    variacion_porcentual = models.FloatField(null=True, blank=True)
    fuente = models.CharField(max_length=50)

    class Meta:
        unique_together = ("pais", "fecha")
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.pais.nombre} - {self.fecha}"