from rest_framework import serializers
from apps.product.models import Product
from apps.product_type.serializers import ProductTypeSerializer


class ProductSerializer(serializers.ModelSerializer):
    _id_typeproduct = ProductTypeSerializer(source="id_typeproduct", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
