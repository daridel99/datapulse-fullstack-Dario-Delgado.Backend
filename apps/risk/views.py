from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.countries.models import Pais
from .services.irpc_service import IRPCService


@api_view(["POST"])
def calcular_riesgo(request):

    resultados = []

    for pais in Pais.objects.all():
        indice = IRPCService.calcular_irpc(pais)

        resultados.append({
            "pais": pais.nombre,
            "indice": indice.indice_compuesto,
            "nivel": indice.nivel_riesgo
        })

    return Response(resultados)