from apps.user.models import *
from apps.company.serializers import *
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        exclude = ["created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    _id_role = RoleSerializer(source="id_role", read_only=True)
    _company_id = CompanySerializer(source="company_id", read_only=True)

    class Meta:
        model = User
        exclude = ["created", "updated", "deleted"]
        extra_kwargs = {"password": {"write_only": True}}


class UserGetSerializer(serializers.ModelSerializer):
    _id_role = RoleSerializer(source="id_role", read_only=True)

    class Meta:
        model = User
        fields = [
            "company_id",
            "id",
            "first_name",
            "last_name",
            "email",
            "id_role",
            "ruc",
            "status",
            "_id_role",
        ]

    extra_kwargs = {"password": {"write_only": True}}


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    # module = ModuleSerializer(source='module_id', read_only=True)
    class Meta:
        model = Permission
        exclude = ["created_at", "updated_at"]


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    def validate_old_password(self, password):
        user = self.context["view"].get_object()
        if not user.check_password(password):
            raise serializers.ValidationError("La contraseña actual no es correcta.")
