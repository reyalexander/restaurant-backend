from apps.user.models import *
from apps.company.serializers import *
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


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
