"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant API",
        default_version="v1",
        description="API para hacer Documentacion de mi proyecto",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="alexandercayromamani@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/company/", include("apps.company.urls")),
    path("api/v1/user/", include("apps.user.urls")),
    path("api/v1/product/", include("apps.product.urls")),
    path("api/v1/product_type/", include("apps.product_type.urls")),
    path("api/v1/resource/", include("apps.resource.urls")),
    path("api/v1/table/", include("apps.table.urls")),
    path("api/v1/ticket/", include("apps.ticket.urls")),
    path("api/v1/ticket_detail/", include("apps.ticket_detail.urls")),
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
