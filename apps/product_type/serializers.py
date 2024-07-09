from rest_framework import serializers
from apps.product_type.models import ProductType


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        exclude = ["created_at", "updated_at", "deleted", "company_id"]


class ProductTypeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "name", "description", "status"]
