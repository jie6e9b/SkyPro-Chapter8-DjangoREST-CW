from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import HabitViewSet, PublicHabitListView

router = SimpleRouter()
router.register(r"", HabitViewSet, basename="habit")

public_router = SimpleRouter()
public_router.register(r"public", PublicHabitListView, basename="public-habits")

urlpatterns = [
    # Public must go first so that /public/ doesn't get captured as a detail route pk
    path("", include(public_router.urls)),
    path("", include(router.urls)),
]
