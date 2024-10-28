from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import SlotMachine,AssetTracker,Model
from django import forms
import pandas as pd
from django.template.response import TemplateResponse

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


def sync_all_asset_trackers(request):
    asset_trackers = AssetTracker.objects.all()
    slot_machines = SlotMachine.objects.select_related('machine_model_name').in_bulk(field_name='machine_serial_number')

    # Use a generator to compare and filter only the changed records
    updated_assets = (
        asset for asset in asset_trackers
        if (
            slot_machine := slot_machines.get(asset.machine_serial_number)
        ) and (
            asset.slot_machine_name != slot_machine.slot_machine_name or
            asset.slot_location != slot_machine.slot_location or
            asset.slot_game_name != slot_machine.slot_game_name or
            asset.machine_model_name != (
                slot_machine.machine_model_name.model_name if slot_machine.machine_model_name else None
            )
        )
    )

    # Update fields in the filtered records only
    to_update = []
    for asset in updated_assets:
        slot_machine = slot_machines.get(asset.machine_serial_number)
        asset.slot_machine_name = slot_machine.slot_machine_name
        asset.slot_location = slot_machine.slot_location
        asset.slot_game_name = slot_machine.slot_game_name
        asset.machine_model_name = (
            slot_machine.machine_model_name.model_name if slot_machine.machine_model_name else None
        )
        to_update.append(asset)

    # Bulk update only if there are changes
    if to_update:
        AssetTracker.objects.bulk_update(
            to_update,
            ['slot_machine_name', 'slot_location', 'slot_game_name', 'machine_model_name']
        )

    messages.success(request, f"Successfully synced {len(to_update)} AssetTracker records.")
    return redirect(reverse('admin:assets_assettracker_changelist'))



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
                'Slot_Denomination': 'slot_denomination',
                'Slot_Denomination_Value': 'slot_denomination_value',
                'Slot_Status': 'status',
                'Machine_Model_Name': 'machine_model_name',
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
                'slot_denomination': 'first',
                'slot_denomination_value': lambda x: ', '.join(map(str, x.unique()))
            }).reset_index()

            # Fetch existing serial numbers and Model instances
            existing_serials = set(SlotMachine.objects.values_list('machine_serial_number', flat=True))
            existing_models = {model.model_name: model for model in Model.objects.all()}

            # Prepare lists for bulk operations
            new_slot_machines = []
            updated_slot_machines = []

            for _, row in grouped_df.iterrows():
                # Get or create the Model instance without hitting the database repeatedly
                model_instance = existing_models.get(row["machine_model_name"])
                if not model_instance:
                    model_instance = Model(model_name=row["machine_model_name"])
                    model_instance.save()
                    existing_models[row["machine_model_name"]] = model_instance

                if row["machine_serial_number"] in existing_serials:
                    # Update existing SlotMachine record
                    updated_slot_machines.append(
                        SlotMachine(
                            machine_serial_number=row["machine_serial_number"],
                            casino_id=row["casino_id"],
                            slot_machine_name=row["slot_machine_name"],
                            slot_location=row["slot_location"],
                            slot_cabinet_name=row["slot_cabinet_name"],
                            slot_game_name=row["slot_game_name"],
                            machine_model_name=model_instance,
                            slot_denomination=row["slot_denomination"],
                            slot_denomination_value=row["slot_denomination_value"],
                            status=row["status"]
                        )
                    )
                else:
                    # Create new SlotMachine record
                    new_slot_machines.append(
                        SlotMachine(
                            machine_serial_number=row["machine_serial_number"],
                            casino_id=row["casino_id"],
                            slot_machine_name=row["slot_machine_name"],
                            slot_location=row["slot_location"],
                            slot_cabinet_name=row["slot_cabinet_name"],
                            slot_game_name=row["slot_game_name"],
                            machine_model_name=model_instance,
                            slot_denomination=row["slot_denomination"],
                            slot_denomination_value=row["slot_denomination_value"],
                            status=row["status"]
                        )
                    )

            # Bulk create new records
            if new_slot_machines:
                SlotMachine.objects.bulk_create(new_slot_machines)

            # Bulk update existing records
            if updated_slot_machines:
                SlotMachine.objects.bulk_update(
                    updated_slot_machines,
                    ['casino_id', 'slot_machine_name', 'slot_location', 'slot_cabinet_name',
                     'slot_game_name', 'machine_model_name', 'slot_denomination',
                     'slot_denomination_value', 'status']
                )

            messages.success(request, "CSV file imported successfully.")
        except Exception as e:
            messages.error(request, f"Error processing CSV: {e}")
        
        return redirect(reverse("admin:assets_slotmachine_changelist"))

    # Render form if GET or no file uploaded
    form = CsvImportForm()
    return render(request, "admin/csv_form.html", {"form": form})

def import_serials(request):
    # Process only if request is POST and contains a file
    if request.method == "POST" and request.FILES.get("csv_upload"):
        csv_file = request.FILES["csv_upload"]

        try:
            # Load the CSV into a DataFrame
            df = pd.read_csv(csv_file)
            # Rename columns to match model field names
            df.rename(columns={'Machine_Serial_Number': 'machine_serial_number'}, inplace=True)

            # Check for required column
            if 'machine_serial_number' not in df.columns:
                messages.error(request, "CSV file does not contain a 'machine_serial_number' column.")
                return redirect(reverse("admin:assets_assettracker_changelist"))

            # Collect unique serials to prevent duplication
            new_serials = []
            existing_serials = set(AssetTracker.objects.values_list('machine_serial_number', flat=True))

            # Loop through unique serial numbers and prepare for bulk creation
            for serial in df['machine_serial_number'].unique():
                if serial not in existing_serials:
                    new_serials.append(AssetTracker(machine_serial_number=serial))

            # Perform bulk create if new serials exist
            if new_serials:
                AssetTracker.objects.bulk_create(new_serials)
                messages.success(request, f"Imported {len(new_serials)} new serial numbers.")
            else:
                messages.info(request, "No new serial numbers to import.")

        except Exception as e:
            # Log the error and notify the user
            messages.error(request, f"Error processing file: {e}")
            print(f"Exception in import_serials: {e}")  # Debugging information

        # Redirect to the changelist after processing
        return redirect(reverse("admin:assets_assettracker_changelist"))

    # Render the form if GET request or no file uploaded
    form = CsvImportForm()
    return render(request, "admin/csv_form.html", {"form": form})

def import_machine_data(request):
    if request.method == "POST" and request.FILES.get("csv_upload"):
        csv_file = request.FILES["csv_upload"]

        try:
            # Load data from CSV file into DataFrame
            df = pd.read_csv(csv_file)
            expected_columns = ['Slot_Cabinet_Name', 'Machine_Model_Name', 'Machine_Manufacturer_Name1']
            if not all(col in df.columns for col in expected_columns):
                messages.error(request, "CSV file is missing required columns.")
                return redirect(reverse("admin:assets_model_changelist"))

            # Step 1: Fetch all existing model names from the database to avoid duplicates
            existing_models = set(Model.objects.values_list("model_name", flat=True))

            # Step 2: Prepare a list of new Model objects for bulk creation
            models_to_create = []
            new_entries = 0

            for _, row in df.iterrows():
                model_name = row['Machine_Model_Name'].strip()  # Assuming this is the unique name
                model_type = row['Slot_Cabinet_Name'].strip()
                manufacturer = row['Machine_Manufacturer_Name1'].strip()

                # Skip if model_name already exists in the database
                if model_name in existing_models:
                    continue

                # Add new entry to the list
                models_to_create.append(
                    Model(
                        model_name=model_name,
                        model_type=model_type,
                        manufacturer=manufacturer,
                    )
                )
                existing_models.add(model_name)  # Update set to avoid duplicates
                new_entries += 1

            # Step 3: Bulk create new entries if there are any
            if models_to_create:
                Model.objects.bulk_create(models_to_create)
                messages.success(request, f"{new_entries} new entries added. Existing entries skipped.")
            else:
                messages.info(request, "No new entries to add.")

        except Exception as e:
            messages.error(request, f"Error reading CSV file: {e}")

        return redirect(reverse("admin:assets_model_changelist"))

    # Render form if GET or no file uploaded
    form = CsvImportForm()
    return render(request, "admin/csv_form.html", {"form": form})