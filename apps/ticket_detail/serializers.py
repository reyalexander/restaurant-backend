from rest_framework import serializers
from apps.ticket_detail.models import TicketDetail
from apps.ticket.serializers import TicketSerializer


class TicketDetailSerializer(serializers.ModelSerializer):
    _ticket_id = TicketSerializer(source="ticket_id", read_only=True)

    class Meta:
        model = TicketDetail
        fields = "__all__"
