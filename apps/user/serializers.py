from apps.user.models import *
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    _id_role = RoleSerializer(source="id_role", read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserGetSerializer(serializers.ModelSerializer):
    _id_role = RoleSerializer(source="id_role", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "id_role",
            "ruc",
            "status",
            "_id_role",
        ]
