from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r"plate_list", views.PlateListViewSet, basename="plate-list")
router.register(r"", views.ProductTypeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
