from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import SlotMachineMaintenanceForm
from assets.models import AssetTracker
from django.db.models import Count
from .serializers import AssetTrackerSerializer, SlotMachineMaintenanceFormSerializer
from django.db.models import Q

class CasinoOutOfServiceView(APIView):
    def get(self, request):
        # Filter distinct casinos, excluding blank or null Casino_IDs
        casinos = AssetTracker.objects.filter(~Q(casino_id=""), casino_id__isnull=False).values('casino_id').distinct()
        response_data = []

        # Calculate the total out-of-service count across all casinos
        total_out_of_service = SlotMachineMaintenanceForm.objects.filter(operational_status='OUT_OF_SERVICE').count()

        for casino in casinos:
            # Filter machines for each casino that are out of service
            machines = SlotMachineMaintenanceForm.objects.filter(
                machine__casino_id=casino['casino_id'],
                operational_status='OUT_OF_SERVICE'
            )
            machine_data = SlotMachineMaintenanceFormSerializer(machines, many=True).data
            response_data.append({
                'casino_id': casino['casino_id'],
                'total_out_of_service': machines.count(),
                'machines': machine_data
            })
        
        return Response({
            'total_out_of_service': total_out_of_service,
            'casinos': response_data
        })