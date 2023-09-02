from rest_framework import serializers
from apps.ticket_detail.models import TicketDetail

class TicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDetail
        fields = '__all__'