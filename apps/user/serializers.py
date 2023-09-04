
from apps.user.models import *
from rest_framework import serializers

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(source='permission_set',many=True,required=False,label='permisos')

    class Meta:
        model  = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','is_admin','last_login','created','updated','groups','user_permissions']
