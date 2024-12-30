from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.utils import timezone
from .models import SlotMachineMaintenanceForm
from .serializers import SlotMachineMaintenanceFormSerializer
from slot_importer.models import SlotMachine
from django.db.models import Q

from django.db import transaction
from rest_framework import status


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated



'''
class CasinoOutOfServiceView(APIView):
    def get(self, request):
        casinos = SlotMachine.objects.filter(~Q(casino_id=""), casino_id__isnull=False).values('casino_id').distinct()
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
'''


class SlotMachineMaintenanceFormViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SlotMachineMaintenanceForm.objects.select_related('machine', 'initiated_by')  # Optimize queries
  #  queryset = SlotMachineMaintenanceForm.objects.all()
    serializer_class = SlotMachineMaintenanceFormSerializer

    def get_queryset(self):
        # Get the user's group name(s)
        user_groups = self.request.user.groups.values_list('name', flat=True)

        # Extract casino_id from the group name
        if not user_groups:
            return SlotMachineMaintenanceForm.objects.none()

        # Filter based on the casino_id
        return SlotMachineMaintenanceForm.objects.filter(machine__casino__casino_id__in=user_groups)
  

    def perform_create(self, serializer):
        # Automatically set the initiated_by field to the logged-in user
        serializer.save(initiated_by=self.request.user)


class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email,
        })
    

class SlotMachineMaintenanceFormCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        machine_id = request.data.get('machine')
        if not machine_id:
            return Response({"detail": "Machine ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            machine = SlotMachine.objects.get(machine_serial_number=machine_id)
        except SlotMachine.DoesNotExist:
            return Response({"detail": "Machine not found."}, status=status.HTTP_404_NOT_FOUND)

        if machine.open_ticket:
            return Response({"detail": "This machine already has an open ticket."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data.pop('initiated_by', None)

        serializer = SlotMachineMaintenanceFormSerializer(data=data)
        if serializer.is_valid():
            maintenance_form = serializer.save(initiated_by=request.user)
            machine.open_ticket = True
            machine.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




