from rest_framework import viewsets, permissions, status
from .models import Role, Permission, User
from .serializers import RoleSerializer, PermissionSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from .filters import *
from rest_framework.response import Response


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [RolViewFilter]

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


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [UserViewFilter]

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


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            user = self.get_user(request.data)
            if user.is_superuser:
                superuser_id = user.id
                response.data["user_id"] = superuser_id

        return response

    def get_user(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
        return None
