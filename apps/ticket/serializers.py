from rest_framework import serializers
from apps.ticket.models import Ticket
from apps.table.serializers import TableSerializer
from apps.user.serializers import UserGetSerializer


class TicketSerializer(serializers.ModelSerializer):
    _table_id = TableSerializer(source="table_id", read_only=True)
    _user_id = UserGetSerializer(source="user_id", read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"
