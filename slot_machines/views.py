from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
#from .models import SlotMachine
from django import forms
import pandas as pd
from django.template.response import TemplateResponse
from django.utils.timezone import now
from django.db import transaction
from casinos.models import Casino

from slot_importer.models import SlotMachine
from .models import EGMSlotMachine

# Create your views here.
#Asset Tracker


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


def sync_all_asset_trackers(request):
    # Fetch all SlotMachine objects with related fields
    asset_trackers = EGMSlotMachine.objects.all()
    slot_machines = SlotMachine.objects.select_related('machine_model_name', 'casino').in_bulk(field_name='machine_serial_number')

    # Initialize an empty list for assets to be updated
    to_update = []

    for asset in asset_trackers:
        slot_machine = slot_machines.get(asset.machine_serial_number)
        if not slot_machine:
            continue  # Skip if no matching slot machine found

        # Compare fields to detect changes
        changes_detected = False
        if asset.slot_machine_name != slot_machine.slot_machine_name:
            asset.slot_machine_name = slot_machine.slot_machine_name
            changes_detected = True
        if asset.casino_id != slot_machine.casino_id:
            asset.casino_id = slot_machine.casino_id
            changes_detected = True
        if asset.slot_location != slot_machine.slot_location:
            asset.slot_location = slot_machine.slot_location
            changes_detected = True
        if asset.slot_game_name != slot_machine.slot_game_name:
            asset.slot_game_name = slot_machine.slot_game_name
            changes_detected = True
        if asset.machine_model_name != (slot_machine.machine_model_name.model_name if slot_machine.machine_model_name else None):
            asset.machine_model_name = slot_machine.machine_model_name.model_name if slot_machine.machine_model_name else None
            changes_detected = True

        if changes_detected:
            to_update.append(asset)

    # Perform bulk update if there are changes
    if to_update:
        EGMSlotMachine.objects.bulk_update(
            to_update,
            ['slot_machine_name', 'casino_id', 'slot_location', 'slot_game_name', 'machine_model_name']
        )
        messages.success(request, f"Successfully synced {len(to_update)} AssetTracker records.")
    else:
        messages.info(request, "No records needed syncing.")

    # Redirect to the admin changelist
    return redirect(reverse('admin:slot_machines_egmslotmachine_changelist'))

#Asset Trackers
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
            existing_serials = set(SlotMachine.objects.values_list('machine_serial_number', flat=True))

            # Loop through unique serial numbers and prepare for bulk creation
            for serial in df['machine_serial_number'].unique():
                if serial not in existing_serials:
                    new_serials.append(SlotMachine(machine_serial_number=serial))

            # Perform bulk create if new serials exist
            if new_serials:
                SlotMachine.objects.bulk_create(new_serials)
                messages.success(request, f"Imported {len(new_serials)} new serial numbers.")
            else:
                messages.info(request, "No new serial numbers to import.")

        except Exception as e:
            # Log the error and notify the user
            messages.error(request, f"Error processing file: {e}")
            print(f"Exception in import_serials: {e}")  # Debugging information

        # Redirect to the changelist after processing
        return redirect(reverse("admin:slot_machines_egmslotmachine_changelist"))


    # Render the form if GET request or no file uploaded
    form = CsvImportForm()
    return render(request, "admin/csv_form.html", {"form": form})
