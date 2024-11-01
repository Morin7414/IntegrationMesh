from rest_framework import serializers
from .models import SlotMachineMaintenanceForm
from assets.models import AssetTracker
from django.utils import timezone
class AssetTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTracker
        fields = ['slot_machine_name', 'machine_serial_number', 'casino_id']  # Include casino ID

class SlotMachineMaintenanceFormSerializer(serializers.ModelSerializer):
    machine = AssetTrackerSerializer(read_only=True)
    days_out_of_service = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SlotMachineMaintenanceForm
        fields = ['operational_status', 'maintenance_status', 'machine','date_created','days_out_of_service']

    def get_days_out_of_service(self, obj):
        # Calculate days out of service based on the current time and `date_created`
        if obj.date_created:
            return (timezone.now() - obj.date_created).days
        return None