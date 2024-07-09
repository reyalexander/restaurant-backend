from rest_framework import serializers
from apps.product.models import Product
from apps.product_type.serializers import ProductTypeViewSerializer


class ProductSerializer(serializers.ModelSerializer):
    _id_typeproduct = ProductTypeViewSerializer(source="id_typeproduct", read_only=True)

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "deleted", "company_id"]


class ProductViewSerializer(serializers.ModelSerializer):
    _id_typeproduct = ProductTypeViewSerializer(source="id_typeproduct", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "_id_typeproduct",
            "id_typeproduct",
            "name",
            "description",
            "price",
            "discount",
            "status",
        ]
