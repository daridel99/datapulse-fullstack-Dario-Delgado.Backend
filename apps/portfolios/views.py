from rest_framework import viewsets
from .models import Portafolio
from .serializers import PortafolioSerializer
from apps.users.permissions import IsAdminOrOwnerOrReadOnly


class PortafolioViewSet(viewsets.ModelViewSet):

    queryset = Portafolio.objects.all()
    serializer_class = PortafolioSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]