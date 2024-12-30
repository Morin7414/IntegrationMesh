from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import SlotMachine
from django import forms
import pandas as pd
from django.utils.timezone import now
from casinos.models import Casino
from machine_models.models import MachineModel
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SlotMachine
from .serializers import SlotMachineSerializer

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

def import_csv(request):

    if request.method == "POST" and request.FILES.get("csv_upload"):
        csv_file = request.FILES["csv_upload"]
        try:
            # Load CSV file into a DataFrame
            df = pd.read_csv(csv_file)

            # Print memory usage of the DataFrame
            memory_usage = df.memory_usage(deep=True)
            total_memory = memory_usage.sum()
            print("\n--- Memory Usage of the DataFrame ---")
            print(memory_usage)
            print(f"\nTotal memory used by the DataFrame: {total_memory / (1024 ** 2):.2f} MB\n")

            # Clean up 'CONVxx' from machine_serial_number using regex
            df['Machine_Serial_Number'] = df['Machine_Serial_Number'].str.replace(r'CONV\d+', '', regex=True)

            # Rename columns to match SlotMachine model
            df.rename(columns={
                'Machine_Serial_Number': 'machine_serial_number',
                'Casino_ID': 'casino_id',
                'Slot_Machine_Name': 'slot_machine_name',
                'Slot_Location': 'slot_location',
                'Slot_Game_Name': 'slot_game_name',
                'Slot_Denomination_Value': 'slot_denomination_value',
                'Slot_Status': 'status',
                'Machine_Model_Name': 'machine_model_name',
            }, inplace=True)

            # Group data for unique serial numbers
            grouped_df = df.groupby('machine_serial_number').agg({
                'casino_id': 'first',
                'slot_machine_name': 'first',
                'slot_location': 'first',
                'slot_game_name': 'first',
                'machine_model_name': 'first',
                'status': 'first',
                'slot_denomination_value': lambda x: ', '.join(map(str, x.unique()))
            }).reset_index()

            # Fetch existing SlotMachine records
            existing_machines = SlotMachine.objects.in_bulk(field_name="machine_serial_number")

            # Cache for Casino and MachineModel lookups
            casino_cache = {casino.casino_id: casino for casino in Casino.objects.all()}
            model_cache = {model.model_name: model for model in MachineModel.objects.all()}

            new_records = []
            updated_records = []

            # Compare and process each record
            for _, row in grouped_df.iterrows():
                serial_number = row["machine_serial_number"]
                if serial_number in existing_machines:
                    slot_machine = existing_machines[serial_number]
                    # Update only if there are changes
                    if (
                        slot_machine.slot_machine_name != row["slot_machine_name"] or
                        slot_machine.slot_location != row["slot_location"] or
                        slot_machine.slot_game_name != row["slot_game_name"] or
                        slot_machine.slot_denomination_value != row["slot_denomination_value"] or
                        slot_machine.status != row["status"]
                    ):
                        # Update SlotMachine fields
                        slot_machine.slot_machine_name = row["slot_machine_name"]
                        slot_machine.slot_location = row["slot_location"]
                        slot_machine.slot_game_name = row["slot_game_name"]
                        slot_machine.slot_denomination_value = row["slot_denomination_value"]
                        slot_machine.status = row["status"]
                        slot_machine.last_updated = now()
                        updated_records.append(slot_machine)
                else:
                    # Get or create the Casino instance
                    casino_instance = casino_cache.get(row["casino_id"])
                    if not casino_instance:
                        casino_instance = Casino.objects.create(casino_id=row["casino_id"], casino_name="Unknown")
                        casino_cache[row["casino_id"]] = casino_instance

                    # Get or create the MachineModel instance
                    model_instance = model_cache.get(row["machine_model_name"])
                    if not model_instance:
                        model_instance = MachineModel.objects.create(model_name=row["machine_model_name"])
                        model_cache[row["machine_model_name"]] = model_instance

                    # Create new SlotMachine record
                    new_records.append(SlotMachine(
                        machine_serial_number=serial_number,
                        casino=casino_instance,
                        slot_machine_name=row["slot_machine_name"],
                        slot_location=row["slot_location"],
                        slot_game_name=row["slot_game_name"],
                        machine_model_name=model_instance,
                        slot_denomination_value=row["slot_denomination_value"],
                        status=row["status"],
                        last_updated=now()
                    ))

            # Save changes to the database
            if new_records:
                SlotMachine.objects.bulk_create(new_records)

            if updated_records:
                SlotMachine.objects.bulk_update(
                    updated_records,
                    ['slot_machine_name', 'slot_location','slot_game_name',
                     'slot_denomination_value', 'status', 'last_updated']
                )

            messages.success(request, f"CSV file imported successfully. New: {len(new_records)}, Updated: {len(updated_records)}")
        except Exception as e:
            messages.error(request, f"Error processing CSV: {e}")
            print(f"Error: {e}")

        return redirect(reverse("admin:slot_importer_slotmachine_changelist"))

    # Render the form if GET request or no file uploaded
    form = CsvImportForm()
    return render(request, "admin/csv_form.html", {"form": form})


class MachineListAPIView(APIView):

    permission_classes = [IsAuthenticated]

  #  def get(self, request):
    #    machines = SlotMachine.objects.all()  # Fetch all machines
     #   serializer = SlotMachineSerializer(machines, many=True)
      #  return Response(serializer.data)

    def get(self, request):
        # Retrieve the group(s) of the authenticated user
        user_groups = request.user.groups.values_list('name', flat=True)
        print(f"Authenticated User: {request.user}")
        print(f"User Groups: {list(user_groups)}")

        if not user_groups:
            print("No groups found for the user.")
            return Response({"detail": "User does not belong to any group."}, status=403)

        # Filter SlotMachine records by group name matching the casino_id
        try:
            machines = SlotMachine.objects.filter(casino__casino_id__in=user_groups)
            print(f"Filtered Machines Count: {machines.count()}")
        except Exception as e:
            print(f"Error in filtering machines: {e}")
            return Response({"detail": "Error filtering machines."}, status=500)

        # Serialize the filtered slot machines
        serializer = SlotMachineSerializer(machines, many=True)
       
        return Response(serializer.data)
    

    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    

    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    

    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    

    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    


    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    


    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    

    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    

    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    

    class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    
class SlotMachineDetailView(RetrieveAPIView):
        queryset = SlotMachine.objects.all()
        serializer_class = SlotMachineSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'machine_serial_number'
    