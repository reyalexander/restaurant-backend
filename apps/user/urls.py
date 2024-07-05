from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PermissionViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r"roles", RoleViewSet)
router.register(r"permissions", PermissionViewSet)
router.register(r"users", UserViewSet)
router.register(r"module", ModuleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_view"),
    path(
        "change-own-password/",
        ChangeOwnUserPasswordView.as_view(),
        name="change_own_user_password",
    ),
    path(
        "bulk-update-permissions/",
        BulkUpdatePermissionsView.as_view({"patch": "update"}),
        name="bulk-update-permissions",
    ),
]
