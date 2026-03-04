from django.urls import path
from .views import calcular_riesgo

urlpatterns = [
    path("calcular/", calcular_riesgo),
]