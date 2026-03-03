from django.db import models
from django.db.models import Q
from apps.countries.models import Pais


class IndiceRiesgo(models.Model):

    class NivelRiesgo(models.TextChoices):
        BAJO = "BAJO"
        MODERADO = "MODERADO"
        ALTO = "ALTO"
        CRITICO = "CRITICO"

    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="indices_riesgo")
    fecha_calculo = models.DateTimeField(auto_now_add=True)

    score_economico = models.FloatField()
    score_cambiario = models.FloatField()
    score_estabilidad = models.FloatField()
    indice_compuesto = models.FloatField()

    nivel_riesgo = models.CharField(max_length=20, choices=NivelRiesgo.choices)
    detalle_calculo = models.JSONField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(indice_compuesto__gte=0) & Q(indice_compuesto__lte=100),
                name="indice_compuesto_entre_0_100"
            )
        ]
        ordering = ["-fecha_calculo"]

    def __str__(self):
        return f"{self.pais.nombre} - {self.indice_compuesto}"