from rest_framework import serializers
from .models import SlotMachineMaintenanceForm
from assets.models import AssetTracker

class AssetTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTracker
        fields = ['slot_machine_name', 'machine_serial_number', 'casino_id']  # Include casino ID

class SlotMachineMaintenanceFormSerializer(serializers.ModelSerializer):
    machine = AssetTrackerSerializer()

    class Meta:
        model = SlotMachineMaintenanceForm
        fields = ['operational_status', 'maintenance_status', 'machine']