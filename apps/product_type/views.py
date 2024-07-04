from .models import ProductType
from .serializers import *
from apps.product.models import Product
from apps.menu.models import Menu
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q
from .filters import *


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [ProductTypeViewFilter]
    filterset_fields = ["name", "description"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset.filter(
                company_id=user.company_id
            )  # El administrador puede ver todos los elementos, incluidos los eliminados
        return queryset.filter(status__in=[1, 2], company_id=user.company_id)

    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.user
        instance.company_id = user.company_id
        instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlateListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        # Obtener todos los tipos de productos publicados
        product_types = ProductType.objects.filter(
            company_id=user.company_id, is_publish=True
        )

        # Obtener todos los menús publicados
        menus = Menu.objects.filter(company_id=user.company_id, is_publish=True)

        # Inicializar la lista de respuesta
        response_data = {"data": []}

        # Procesar tipos de productos
        for product_type in product_types:
            # Obtener los productos publicados para cada tipo de producto
            products = Product.objects.filter(
                id_typeproduct=product_type, is_publish=True
            )

            # Crear una estructura de datos para el tipo de producto y sus productos
            type_data = {
                "product_type": product_type.name,
                "description": product_type.description,
                "product_image": (
                    product_type.product_image.url
                    if product_type.product_image
                    else None
                ),
                "products": [],
            }

            for product in products:
                product_data = {
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "discount": product.discount,
                    "image": (
                        product.product_type_image.url
                        if product.product_type_image
                        else None
                    ),
                }
                type_data["products"].append(product_data)

            response_data["data"].append(type_data)

        # Agregar una sección para todos los menús bajo el tipo "Menu"
        menu_type_data = {
            "product_type": "Menu",
            "description": "Various menus available",
            "product_image": None,
            "products": [],
        }

        for menu in menus:
            menu_data = {
                "name": menu.name,
                "description": menu.description,
                "price": menu.price,
                "day": menu.get_day_display(),
                "starters": [starter.name for starter in menu.starters.all()],
                "main_courses": [
                    main_course.name for main_course in menu.main_courses.all()
                ],
            }

            menu_type_data["products"].append(menu_data)

        response_data["data"].append(menu_type_data)

        return Response(response_data)
