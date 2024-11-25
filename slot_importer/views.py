from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import SlotMachine
from django import forms
import pandas as pd
from django.utils.timezone import now
from casinos.models import Casino
from machine_models.models import MachineModel

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

def import_csv(request):
    if request.method == "POST" and request.FILES.get("csv_upload"):
        csv_file = request.FILES["csv_upload"]
        try:
            # Load and rename columns for SlotMachine model
            df = pd.read_csv(csv_file)
            df.rename(columns={
                'Machine_Serial_Number': 'machine_serial_number',
                'Casino_ID': 'casino_id',
                'Slot_Machine_Name': 'slot_machine_name',
                'Slot_Location': 'slot_location',
                'Slot_Cabinet_Name': 'slot_cabinet_name',
                'Slot_Game_Name': 'slot_game_name',
                'Slot_Denomination_Value': 'slot_denomination_value',
                'Slot_Status': 'status',
                'Machine_Model_Name': 'machine_model_name',
                'Machine_Manufacturer_Name1': 'machine_manufacturer_name1'
            }, inplace=True)

            # Group denomination values for each unique serial number
            grouped_df = df.groupby('machine_serial_number').agg({
                'casino_id': 'first',
                'slot_machine_name': 'first',
                'slot_location': 'first',
                'slot_cabinet_name': 'first',
                'slot_game_name': 'first',
                'machine_model_name': 'first',
                'status': 'first',
                'machine_manufacturer_name1': 'first',
                'slot_denomination_value': lambda x: ', '.join(map(str, x.unique()))
            }).reset_index()

            # Fetch existing serial numbers and Model instances
            existing_serials = set(SlotMachine.objects.values_list('machine_serial_number', flat=True))
            csv_serials = set(grouped_df['machine_serial_number'])
            serials_to_offline = existing_serials - csv_serials  # Serial numbers in DB but not in CSV

            # Update SlotMachine records to "OFFLINE" if not in CSV
            SlotMachine.objects.filter(machine_serial_number__in=serials_to_offline).update(
                status="OFFLINE",
                last_updated=now()
            )

            # Cache for Casino and Model lookups
            casino_cache = {casino.casino_id: casino for casino in Casino.objects.all()}
            model_cache = {model.model_name: model for model in MachineModel.objects.all()}

            # Prepare lists for bulk operations
            new_slot_machines = []
            updated_slot_machines = []

            for _, row in grouped_df.iterrows():
                # Get or create the Casino instance
                casino_instance = casino_cache.get(row["casino_id"])
                if not casino_instance:
                    casino_instance = Casino.objects.create(casino_id=row["casino_id"], casino_name="Unknown")
                    casino_cache[row["casino_id"]] = casino_instance

                # Get or create the Model instance
                model_instance = model_cache.get(row["machine_model_name"])
                if not model_instance:
                    model_instance = MachineModel.objects.create(model_name=row["machine_model_name"])
                    model_cache[row["machine_model_name"]] = model_instance

                if row["machine_serial_number"] in existing_serials:
                    # Update existing SlotMachine record
                    slot_machine = SlotMachine.objects.get(machine_serial_number=row["machine_serial_number"])
                    slot_machine.casino = casino_instance
                    slot_machine.slot_machine_name = row["slot_machine_name"]
                    slot_machine.slot_location = row["slot_location"]
                    slot_machine.slot_cabinet_name = row["slot_cabinet_name"]
                    slot_machine.slot_game_name = row["slot_game_name"]
                    slot_machine.machine_model_name = model_instance
                    slot_machine.slot_denomination_value = row["slot_denomination_value"]
                    slot_machine.machine_manufacturer_name1 = row["machine_manufacturer_name1"]
                    slot_machine.status = row["status"]
                    slot_machine.last_updated = now()  # Update timestamp
                    updated_slot_machines.append(slot_machine)
                else:
                    # Create new SlotMachine record
                    new_slot_machines.append(
                        SlotMachine(
                            machine_serial_number=row["machine_serial_number"],
                            casino=casino_instance,
                            slot_machine_name=row["slot_machine_name"],
                            slot_location=row["slot_location"],
                            slot_cabinet_name=row["slot_cabinet_name"],
                            slot_game_name=row["slot_game_name"],
                            machine_model_name=model_instance,
                            slot_denomination_value=row["slot_denomination_value"],
                            machine_manufacturer_name1=row["machine_manufacturer_name1"],
                            status=row["status"],
                            last_updated=now()  # Set timestamp for new records
                        )
                    )

            # Bulk create new records
            if new_slot_machines:
                SlotMachine.objects.bulk_create(new_slot_machines)

            # Bulk update existing records
            if updated_slot_machines:
                SlotMachine.objects.bulk_update(
                    updated_slot_machines,
                    ['casino', 'slot_machine_name', 'slot_location', 'slot_cabinet_name',
                     'slot_game_name', 'machine_model_name', 'slot_denomination_value',
                     'machine_manufacturer_name1', 'status', 'last_updated']
                )

            messages.success(request, "CSV file imported successfully.")
        except Exception as e:
            messages.error(request, f"Error processing CSV: {e}")
            print(f"Error: {e}")

        return redirect(reverse("admin:slot_importer_slotmachine_changelist"))

    # Render form if GET or no file uploaded
    form = CsvImportForm()
    return render(request, "admin/csv_form.html", {"form": form})


