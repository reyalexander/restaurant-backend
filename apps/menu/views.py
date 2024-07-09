from .models import *
from .serializers import *
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q
from .filters import *


# Create your views here.
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [MenuViewFilter]

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
