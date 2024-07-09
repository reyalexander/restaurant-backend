from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import *
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q
from .filters import *


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [CompanyViewFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset  # El administrador puede ver todos los elementos, incluidos los eliminados
        return queryset.filter(status__in=[1, 2])
