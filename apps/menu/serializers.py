from rest_framework import serializers
from apps.product.models import Product
from apps.product_type.serializers import ProductTypeSerializer


from rest_framework import serializers
from .models import Menu
from apps.product.serializers import ProductViewSerializer


class MenuSerializer(serializers.ModelSerializer):
    _starters = ProductViewSerializer(many=True, source="starters", read_only=True)
    _main_courses = ProductViewSerializer(
        many=True, source="main_courses", read_only=True
    )

    class Meta:
        model = Menu
        exclude = ["created_at", "updated_at", "company_id"]
