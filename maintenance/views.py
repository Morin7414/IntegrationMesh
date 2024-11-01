from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import SlotMachineMaintenanceForm
from .serializers import SlotMachineMaintenanceFormSerializer
from assets.models import AssetTracker
from django.db.models import Q

class CasinoOutOfServiceView(APIView):
    def get(self, request):
        casinos = AssetTracker.objects.filter(~Q(casino_id=""), casino_id__isnull=False).values('casino_id').distinct()
        response_data = []

        total_out_of_service = SlotMachineMaintenanceForm.objects.filter(operational_status='OUT_OF_SERVICE').count()

        for casino in casinos:
            machines = SlotMachineMaintenanceForm.objects.filter(
                machine__casino_id=casino['casino_id'],
                operational_status='OUT_OF_SERVICE'
            )

            # Use serializer to ensure all fields are included
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
