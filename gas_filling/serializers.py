from rest_framework import serializers
from .models import Tank, Pump, Refuel

class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = '__all__'

class PumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pump
        fields = '__all__'

class RefuelSerializer(serializers.ModelSerializer):
    refuel_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Refuel
        fields = 'id', 'amount_display', 'tax_display', 'liters_formatted', 'refuel_date', 'pump'