from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from machine_models.models import MachineModel
from django import forms
import pandas as pd

from django.utils.timezone import now



class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()



#Slot Models
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
            existing_models = set(MachineModel.objects.values_list("model_name", flat=True))

            # Step 2: Prepare a list of new Model objects for bulk creation
            models_to_create = []
            new_entries = 0

            for _, row in df.iterrows():
                model_name = str(row['Machine_Model_Name']).strip() if pd.notna(row['Machine_Model_Name']) else ''
                model_type = str(row['Slot_Cabinet_Name']).strip() if pd.notna(row['Slot_Cabinet_Name']) else ''
                manufacturer = str(row['Machine_Manufacturer_Name1']).strip() if pd.notna(row['Machine_Manufacturer_Name1']) else ''

                # Skip if model_name is empty or already exists in the database
                if not model_name or model_name in existing_models:
                    continue

                # Add new entry to the list
                models_to_create.append(
                    MachineModel(
                        model_name=model_name,
                        model_type=model_type,
                        manufacturer=manufacturer,
                    )
                )
                existing_models.add(model_name)  # Update set to avoid duplicates
                new_entries += 1

            # Step 3: Bulk create new entries if there are any
            if models_to_create:
                MachineModel.objects.bulk_create(models_to_create)
                messages.success(request, f"{new_entries} new entries added. Existing entries skipped.")
            else:
                messages.info(request, "No new entries to add.")

        except Exception as e:
            messages.error(request, f"Error reading CSV file: {e}")

        return redirect(reverse("admin:machine_models_machinemodel_changelist"))

    # Render form if GET or no file uploaded
    form = CsvImportForm()
    return render(request, "admin/csv_form.html", {"form": form})