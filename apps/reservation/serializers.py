from rest_framework import serializers
from .models import *
from apps.user.serializers import UserGetSerializer


class ReservationSerializer(serializers.ModelSerializer):
    _user_id = UserGetSerializer(source="user_id", read_only=True)

    class Meta:
        model = Reservation
        exclude = ["created", "updated"]

    def delete(self):
        self.status = 3
        self.save()
