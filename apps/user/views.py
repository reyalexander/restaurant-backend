from rest_framework import viewsets, permissions, status, generics, response
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from .filters import *
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash


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
        user = self.request.user
        instance = serializer.save(company_id=user.company_id)
        instance.full_name = (
            serializer.validated_data["first_name"]
            + " "
            + serializer.validated_data["last_name"]
        )
        # Hashear la contraseña antes de guardar el usuario
        instance.password = make_password(serializer.validated_data["password"])
        instance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            user = self.get_user(request.data)
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


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["module_id", "module_name", "status"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset  # El administrador puede ver todos los elementos, incluidos los eliminados
        return queryset.filter(status__in=[1, 2])

    def create(self, request, *args, **kwargs):

        if not (
            request.user.is_superuser
            or obtener_permise_create(request.user.role_id.id, 1)
        ):
            return Response(
                {"error": "No tienes permisos para añadir un módulo"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Si el usuario tiene los permisos, continuar con la creación del objeto
        return super().create(request, *args, **kwargs)


def obtener_permise_create(role_id, modulo_id):
    # Filtrar los permisos y obtener el primer objeto
    permiso = Permission.objects.filter(role_id=role_id, module_id=modulo_id).first()
    # Verificar si se encontró un permiso
    if permiso:
        # Retornar el valor de 'notify'
        return permiso.create
    else:
        # Si no se encontró ningún permiso, retornar None o lanzar una excepción según sea necesario
        return False


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "module_id",
        "role_id",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset.order_by(
                "id"
            )  # El administrador puede ver todos los elementos, incluidos los eliminados
        return queryset.order_by("id")

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializers = [self.get_serializer(data=item) for item in data]
            valid = all(serializer.is_valid() for serializer in serializers)
            if valid:
                permissions = [serializer.save() for serializer in serializers]
                return Response(
                    PermissionSerializer(permissions, many=True).data,
                    status=status.HTTP_201_CREATED,
                )
            else:
                errors = [serializer.errors for serializer in serializers]
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )


class BulkUpdatePermissionsView(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        data = request.data

        # Valida que la solicitud sea una lista de objetos JSON
        if not isinstance(data, list):
            return Response(
                "La solicitud debe contener una lista de objetos JSON.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Itera a través de los objetos JSON y actualiza los permisos correspondientes
        updated_permissions = []
        for item in data:
            permission_id = item.get("id")
            try:
                permission = Permission.objects.get(id=permission_id)
                serializer = self.get_serializer(permission, data=item, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                updated_permissions.append(serializer.data)
            except Permission.DoesNotExist:
                return Response(
                    f"Permiso con ID {permission_id} no encontrado.",
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(updated_permissions, status=status.HTTP_200_OK)


class ChangeOwnUserPasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve the currently logged-in user
        user = self.request.user

        # Return a queryset containing only the currently logged-in user
        return User.objects.filter(pk=user.pk)

    def update(self, request, *args, **kwargs):
        # Obtén el usuario actual a través de la solicitud
        user = self.request.user

        # Verifica si se proporciona la contraseña actual
        old_password = request.data.get("password")
        if old_password and not user.check_password(old_password):
            return Response(
                {"detail": "La contraseña actual proporcionada es incorrecta."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Procesa la solicitud de cambio de contraseña
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            # Actualiza la sesión del usuario para evitar cerrar la sesión después de cambiar la contraseña
            update_session_auth_hash(request, user)

            return Response(
                {"detail": "Contraseña cambiada con éxito."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSuperUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Obtén el usuario a través del ID proporcionado en la solicitud
        user_id = kwargs.get("pk")
        user = User.objects.get(pk=user_id)

        # Verifica si el usuario actual está autenticado y este es admin
        if not request.user.is_authenticated or not request.user.is_admin:
            return Response(
                {
                    "detail": "No tienes permisos para cambiar la contraseña de este usuario."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        # Procesa la solicitud de cambio de contraseña
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {
                    "detail": "User "
                    + str(user.id)
                    + " - Contraseña cambiada con éxito."
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
