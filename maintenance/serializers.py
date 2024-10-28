from rest_framework import serializers
from .models import SlotMachineMaintenanceForm

class SlotMachineMaintenanceFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotMachineMaintenanceForm
        fields = '__all__'