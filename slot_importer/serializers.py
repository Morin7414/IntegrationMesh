from rest_framework import serializers
from .models import SlotMachine

class SlotMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotMachine
        fields = '__all__'