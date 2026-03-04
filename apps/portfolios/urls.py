from rest_framework.routers import DefaultRouter
from .views import PortafolioViewSet

router = DefaultRouter()
router.register(r"", PortafolioViewSet)

urlpatterns = router.urls