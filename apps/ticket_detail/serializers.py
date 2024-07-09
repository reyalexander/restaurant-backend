from rest_framework import serializers
from apps.ticket_detail.models import TicketDetail
from apps.ticket.serializers import TicketSerializer
from apps.product.serializers import ProductSerializer, Product
from apps.menu.serializers import MenuSerializer, Menu


class TicketDetailSerializer(serializers.ModelSerializer):
    _ticket_id = TicketSerializer(source="ticket_id", read_only=True)
    _product_id = serializers.SerializerMethodField()

    class Meta:
        model = TicketDetail
        fields = "__all__"

    def get__product_id(self, obj):
        if obj.is_menu:
            menu = Menu.objects.get(id=obj.product_id)
            return MenuSerializer(menu).data
        else:
            product = Product.objects.get(id=obj.product_id)
            return ProductSerializer(product).data
