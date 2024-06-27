from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"detail", views.TicketDetailViewSet)
router.register(r"option", views.MenuProductViewSet, basename="menu-product")
urlpatterns = [
    path("", include(router.urls)),
]
