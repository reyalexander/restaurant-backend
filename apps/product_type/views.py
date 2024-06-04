from .models import ProductType
from .serializers import ProductTypeSerializer
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
