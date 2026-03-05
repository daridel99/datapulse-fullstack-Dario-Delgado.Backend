from apps.indicators.models import IndicadorEconomico
from apps.exchange.models import TipoCambio
from apps.risk.models import IndiceRiesgo


class IRPCService:

    @staticmethod
    def calcular_score_economico(pais):

        inflacion = IRPCService.obtener_indicador(pais, "INFLACION")
        desempleo = IRPCService.obtener_indicador(pais, "DESEMPLEO")
        deuda = IRPCService.obtener_indicador(pais, "DEUDA_PIB")
        balanza = IRPCService.obtener_indicador(pais, "BALANZA_COMERCIAL")

        if inflacion is None or desempleo is None or deuda is None or balanza is None:
            return 50

        score = 0

        if inflacion < 5:
            score += 25
        elif inflacion < 10:
            score += 15
        else:
            score += 5

        if desempleo < 6:
            score += 25
        elif desempleo < 10:
            score += 15
        else:
            score += 5

        if deuda < 50:
            score += 25
        elif deuda < 80:
            score += 15
        else:
            score += 5

        if balanza > 0:
            score += 25
        else:
            score += 10

        return min(score, 100)

    @staticmethod
    def calcular_score_cambiario(pais):

        cambios = TipoCambio.objects.filter(pais=pais).order_by("-fecha")[:2]

        if cambios.count() < 2:
            return 50

        actual = cambios[0].tasa
        anterior = cambios[1].tasa

        variacion = abs((actual - anterior) / anterior) * 100

        if variacion < 1:
            return 90
        elif variacion < 3:
            return 70
        elif variacion < 5:
            return 50
        else:
            return 20

    @staticmethod
    def calcular_score_estabilidad(pais):

        pib_pc = IRPCService.obtener_indicador(pais, "PIB_PERCAPITA")

        if pib_pc is None:
            return 50

        if pib_pc > 20000:
            return 90
        elif pib_pc > 10000:
            return 70
        elif pib_pc > 5000:
            return 50
        else:
            return 30

    @staticmethod
    def calcular_indice_compuesto(score_economico, score_cambiario, score_estabilidad):

        return (
            (score_economico * 0.40)
            + (score_cambiario * 0.30)
            + (score_estabilidad * 0.30)
        )

    @staticmethod
    def clasificar_riesgo(indice):

        if indice >= 75:
            return "BAJO"
        elif indice >= 50:
            return "MODERADO"
        elif indice >= 25:
            return "ALTO"
        else:
            return "CRITICO"

    @staticmethod
    def calcular_irpc(pais):

        score_economico = IRPCService.calcular_score_economico(pais)
        score_cambiario = IRPCService.calcular_score_cambiario(pais)
        score_estabilidad = IRPCService.calcular_score_estabilidad(pais)

        indice = IRPCService.calcular_indice_compuesto(
            score_economico,
            score_cambiario,
            score_estabilidad
        )

        nivel = IRPCService.clasificar_riesgo(indice)

        return IndiceRiesgo.objects.create(
            pais=pais,
            score_economico=score_economico,
            score_cambiario=score_cambiario,
            score_estabilidad=score_estabilidad,
            indice_compuesto=indice,
            nivel_riesgo=nivel,
            detalle_calculo={
                "economico": score_economico,
                "cambiario": score_cambiario,
                "estabilidad": score_estabilidad
            }
        )
    
    @staticmethod
    def obtener_indicador(pais, tipo):

        indicador = (
            IndicadorEconomico.objects
            .filter(pais=pais, tipo=tipo)
            .order_by("-anio")
            .values_list("valor", flat=True)
            .first()
        )

        return indicador