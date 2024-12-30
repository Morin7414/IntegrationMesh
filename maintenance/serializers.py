from rest_framework import serializers
from .models import SlotMachineMaintenanceForm
from slot_importer.models import SlotMachine
from django.utils import timezone



'''
class AssetTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotMachine
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
'''


class SlotMachineMaintenanceFormSerializer(serializers.ModelSerializer):
    slot_machine_name = serializers.CharField(source='machine.slot_machine_name', read_only=True)
    machine_model_name = serializers.CharField(source='machine.machine_model_name', read_only=True)  # New field
    slot_location = serializers.CharField(source='machine.slot_location', read_only=True)  # New field

    initiated_by_username = serializers.CharField(source='initiated_by.username', read_only=True)
    
    class Meta:
        model = SlotMachineMaintenanceForm
        fields = [
            'id',
            'machine',
            'slot_machine_name',  # Added for machine name
            'slot_location',  # Added field
            'machine_model_name',  # Added field
            'first_observations',
            'operational_status',
            'maintenance_status',
            'date_created',
            'initiated_by',
            'initiated_by_username',  # Added for username
        ]

    def validate_machine(self, value):
        print("Validating machine:", value)
        if not value:
            raise serializers.ValidationError("A machine must be selected.")
        return value
    
