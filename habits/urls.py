from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import HabitViewSet, PublicHabitListView

router = SimpleRouter()
router.register(r"", HabitViewSet, basename="habit")

urlpatterns = [
    # Публичный список — обычное APIView
    path("public/", PublicHabitListView.as_view(), name="public-habits"),

    # Остальные маршруты ViewSet
    path("", include(router.urls)),
]
