from rest_framework import serializers

from core import models


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rental
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    rental = RentalSerializer()

    class Meta:
        model = models.Event
        fields = '__all__'
