from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SlotMachineMaintenanceForm
from django.db.models import Count

class MaintenanceStatusCountView(APIView):

    def get(self, request):
        # Count each maintenance status by operational status
        status_counts = (
            SlotMachineMaintenanceForm.objects
            .values('operational_status', 'maintenance_status')
            .annotate(count=Count('maintenance_status'))
        )
        
        # Structure the data for clarity in JSON response
        response_data = {
            "IN_SERVICE": {},
            "OUT_OF_SERVICE": {}
        }
        
        # Organize counts by operational and maintenance status
        for entry in status_counts:
            operational_status = entry['operational_status']
            maintenance_status = entry['maintenance_status']
            count = entry['count']
            
            if operational_status in response_data:
                response_data[operational_status][maintenance_status] = count
        
        return Response(response_data)
    

class CasinoOutOfServiceCountView(APIView):
    def get(self, request):
        # Aggregate out-of-service counts by casino_id through machine relationship
        out_of_service_counts = (
            SlotMachineMaintenanceForm.objects
            .filter(operational_status='OUT_OF_SERVICE')
            .values('machine__casino_id')  # Access casino_id through machine
            .annotate(count=Count('id'))
            .order_by('machine__casino_id')
        )

        # Prepare response data, setting zero for any Casino_ID without out-of-service machines
        response_data = {entry['machine__casino_id']: entry['count'] for entry in out_of_service_counts}
        
        # Include all Casino_IDs, setting to zero if there are no out-of-service machines
        all_casinos = set(SlotMachineMaintenanceForm.objects.values_list('machine__casino_id', flat=True))
        for casino_id in all_casinos:
            response_data.setdefault(casino_id, 0)

        return Response(response_data)