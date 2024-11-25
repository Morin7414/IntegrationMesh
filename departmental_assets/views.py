from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import DepartmentalAsset
from machine_models.models import MachineModel
from django import forms
import pandas as pd
from django.template.response import TemplateResponse
from django.utils.timezone import now
from django.db import transaction
from casinos.models import Casino

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()



# Create your views here.
def import_operational_assets(request):
    if request.method == "POST":
        form = CsvImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_upload']
            try:
                print(f"Uploaded File: {csv_file.name}")
                df = pd.read_csv(csv_file)

                df.rename(columns={
                    'Casino_ID': 'casino_id',
                    'Machine_Name': 'machine_name',
                    'Machine_Serial_Number': 'machine_serial_number',
                    'Machine_Model_Name': 'machine_model_name',
                    'Machine_Manufacturer_Name1': 'machine_manufacturer_name1',
                    'Status': 'status'
                }, inplace=True)
                print("Columns renamed successfully.")

                required_columns = ['casino_id', 'machine_name', 'machine_serial_number', 'machine_model_name', 'machine_manufacturer_name1', 'status']
                missing_columns = [col for col in required_columns if col not in df.columns]

                if missing_columns:
                    print(f"Missing columns: {missing_columns}")
                    raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

                # Cache for Casino and Model lookups
                casino_cache = {casino.casino_id: casino for casino in Casino.objects.all()}
                model_cache = {model.model_name: model for model in MachineModel.objects.all()}

                existing_assets = DepartmentalAsset.objects.filter(
                    machine_serial_number__in=df['machine_serial_number']
                ).values_list('machine_serial_number', flat=True)
                print(f"Existing Assets Found: {len(existing_assets)}")

                df_new = df[~df['machine_serial_number'].isin(existing_assets)]
                df_existing = df[df['machine_serial_number'].isin(existing_assets)]

                print(f"New Records to Create: {len(df_new)}")
                print(f"Existing Records to Update: {len(df_existing)}")

                # Bulk create new records
                records_to_create = []
                for _, row in df_new.iterrows():
                    # Lookup or create the Casino instance
                    casino_instance = casino_cache.get(row['casino_id'])
                    if not casino_instance:
                        casino_instance = Casino.objects.create(casino_id=row['casino_id'], casino_name="Unknown")
                        casino_cache[row['casino_id']] = casino_instance  # Update cache

                    # Lookup or create the Model instance
                    model_instance = model_cache.get(row['machine_model_name'])
                    if not model_instance:
                        model_instance =  MachineModel.objects.create(model_name=row['machine_model_name'])
                        model_cache[row['machine_model_name']] = model_instance  # Update cache

                    records_to_create.append(
                        DepartmentalAsset(
                            machine_serial_number=row['machine_serial_number'],
                            casino=casino_instance,
                            machine_name=row['machine_name'],
                            machine_model_name=model_instance,  # Assign the Model instance
                            machine_manufacturer_name1=row['machine_manufacturer_name1'],
                            status=row['status'],
                            last_updated=now(),
                        )
                    )

                # Prepare data for updates
                records_to_update = []
                existing_asset_objects = DepartmentalAsset.objects.filter(
                    machine_serial_number__in=df_existing['machine_serial_number']
                ).in_bulk(field_name='machine_serial_number')

                for _, row in df_existing.iterrows():
                    asset = existing_asset_objects[row['machine_serial_number']]

                    # Lookup or create the Casino instance
                    casino_instance = casino_cache.get(row['casino_id'])
                    if not casino_instance:
                        casino_instance = Casino.objects.create(casino_id=row['casino_id'], casino_name="Unknown")
                        casino_cache[row['casino_id']] = casino_instance  # Update cache

                    # Lookup or create the Model instance
                    model_instance = model_cache.get(row['machine_model_name'])
                    if not model_instance:
                        model_instance =  MachineModel.objects.create(model_name=row['machine_model_name'])
                        model_cache[row['machine_model_name']] = model_instance  # Update cache

                    asset.casino = casino_instance
                    asset.machine_name = row['machine_name']
                    asset.machine_model_name = model_instance  # Assign the Model instance
                    asset.machine_manufacturer_name1 = row['machine_manufacturer_name1']
                    asset.status = row['status']
                    asset.last_updated = now()
                    records_to_update.append(asset)

                # Perform bulk operations
                with transaction.atomic():
                    if records_to_create:
                        DepartmentalAsset.objects.bulk_create(records_to_create, batch_size=500)
                        print(f"Bulk create completed for {len(records_to_create)} records.")
                    if records_to_update:
                        DepartmentalAsset.objects.bulk_update(records_to_update, [
                            'casino', 'machine_name', 'machine_model_name',
                            'machine_manufacturer_name1', 'status', 'last_updated'
                        ], batch_size=500)
                        print(f"Bulk update completed for {len(records_to_update)} records.")

                messages.success(request, f"Data imported successfully. Created: {len(records_to_create)}, Updated: {len(records_to_update)}")
            except Exception as e:
                messages.error(request, f"Error importing data: {e}")
                print(f"Error: {e}")
            return redirect(reverse("admin:departmental_assets_departmentalasset_changelist"))
        else:
            print("Form is invalid.")
            messages.error(request, "Form submission failed. Please try again.")
    else:
        print("GET request received; rendering form.")
        form = CsvImportForm()

    return render(request, "admin/csv_form.html", {"form": form})