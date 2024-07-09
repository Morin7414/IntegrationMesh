# views.py
import csv
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from .forms import CSVUploadForm
from .models import SlotMachine, Model
from django.db import transaction,IntegrityError
import traceback

from django.contrib import messages

def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                decoded_file = csv_file.read().decode('utf-8')
                if decoded_file.startswith('\ufeff'):
                    decoded_file = decoded_file.lstrip('\ufeff')
                reader = csv.DictReader(decoded_file.splitlines())
                csv_data = list(reader)

                existing_data = {sm.machine_serial_number: sm for sm in SlotMachine.objects.all()}
                model_instances = {model.model_name: model for model in Model.objects.all()}
                csv_serial_numbers = {row['Machine_Serial_Number'].strip() for row in csv_data}

                current_time = now()
                updates = []
                new_records = []

                for serial_number, db_row in existing_data.items():
                    if serial_number not in csv_serial_numbers and db_row.status != 'offline':
                        db_row.status = 'offline'
                        db_row.last_updated = current_time
                        updates.append({
                            'machine_serial_number': db_row.machine_serial_number,
                            'changes': {
                                'status': 'offline',
                                'last_updated': current_time.isoformat()
                            }
                        })

                for csv_row in csv_data:
                    serial_number = csv_row.get('Machine_Serial_Number', '').strip()
                    if not serial_number:
                        continue

                    if serial_number in existing_data:
                        db_row = existing_data[serial_number]
                        updated = False
                        for field in csv_row:
                            model_field = field.lower()
                            db_value = getattr(db_row, model_field, None)
                            csv_value = csv_row[field].strip()

                            if model_field == 'slot_denomination_value':
                                db_value = float(db_value) if db_value is not None else None
                                csv_value = float(csv_value)
                            elif model_field == 'gaming_day_count':
                                db_value = int(db_value) if db_value is not None else None
                                csv_value = int(csv_value)
                            elif model_field == 'machine_model_name':
                                db_value = db_value.model_name if db_value else None
                                csv_value = model_instances.get(csv_value).model_name if csv_value in model_instances else None

                            if db_value != csv_value:
                                setattr(db_row, model_field, csv_value)
                                updated = True

                        if db_row.status != 'online':
                            db_row.status = 'online'
                            updated = True

                        if updated:
                            db_row.last_updated = current_time
                            db_row.save()
                    else:
                        new_record = SlotMachine(
                            machine_serial_number=serial_number,
                            casino_id=csv_row.get('Casino_ID', '').strip(),
                            slot_machine_name=csv_row.get('Slot_Machine_Name', '').strip(),
                            slot_location=csv_row.get('Slot_Location', '').strip(),
                            slot_cabinet_name=csv_row.get('Slot_Cabinet_Name', '').strip(),
                            textbox34=csv_row.get('Textbox34', '').strip(),
                            slot_game_name=csv_row.get('Slot_Game_Name', '').strip(),
                            machine_model_name=model_instances.get(csv_row.get('Machine_Model_Name', '').strip()) if csv_row.get('Machine_Model_Name', '').strip() else None,
                            machine_manufacturer_name1=csv_row.get('Machine_Manufacturer_Name1', '').strip(),
                            slot_denomination=csv_row.get('Slot_Denomination', '').strip(),
                            slot_denomination_value=float(csv_row.get('Slot_Denomination_Value', '').strip() or 0),
                            textbox46=csv_row.get('Textbox46', '').strip(),
                            gaming_day_count=int(csv_row.get('Gaming_Day_Count', '').strip() or 0),
                            last_updated=current_time,
                            status='online'
                        )
                        try:
                            new_record.save()
                        except IntegrityError as e:
                            print(f"Integrity Error: {e}")
                            print(traceback.format_exc())
                            return JsonResponse({"error": f"Database integrity error: {str(e).split('\\n')[0]}"}, status=500)

                request.session['updates'] = updates
                request.session['new_records'] = [record.machine_serial_number for record in new_records]
                request.session['csv_file'] = csv_file.name

                messages.success(request, "CSV file imported successfully")
                return redirect('admin:show_updates')
            except Exception as e:
                print(f"Error processing CSV file: {e}")
                print(traceback.format_exc())
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "Form is not valid"}, status=400)
    else:
        form = CSVUploadForm()
    return render(request, 'admin/upload_csv.html', {'form': form})

def show_updates(request):
    updates = request.session.get('updates', [])
    new_records = request.session.get('new_records', [])
    csv_file = request.session.get('csv_file', '')

    return render(request, 'admin/show_updates.html', {
        'updates': updates,
        'new_records': new_records,
        'csv_file': csv_file
    })

def confirm_updates(request):
    updates = request.session.get('updates', [])
    new_records = request.session.get('new_records', [])

    if request.method == "POST":
        try:
            with transaction.atomic():
                for update in updates:
                    try:
                        db_row = SlotMachine.objects.get(machine_serial_number=update['machine_serial_number'])
                        for field, value in update['changes'].items():
                            setattr(db_row, field, value)
                        db_row.save()
                    except Exception as e:
                        print(f"Error updating record with serial number {update['machine_serial_number']}: {e}")
                        print(traceback.format_exc())
                        return JsonResponse({"error": f"Error updating record with serial number {update['machine_serial_number']}: {e}"}, status=500)

                for serial_number in new_records:
                    try:
                        new_record = SlotMachine.objects.get(machine_serial_number=serial_number)
                        new_record.save()
                    except IntegrityError as e:
                        print(f"Integrity Error: {e}")
                        print(traceback.format_exc())
                        return JsonResponse({"error": f"Database integrity error: {str(e).split('\n')[0]}"}, status=500)

            request.session.pop('updates', None)
            request.session.pop('new_records', None)
            request.session.pop('csv_file', None)

            return redirect('admin:success')
        except Exception as e:
            print(f"Error applying updates: {e}")
            print(traceback.format_exc())
            return JsonResponse({"error": f"Error applying updates: {e}"}, status=500)

    return render(request, 'admin/confirm_updates.html', {
        'updates': updates,
        'new_records': new_records
    })

def success(request):
    return render(request, 'admin/success.html')

def import_csv_view(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            new_records = []
            existing_records = {record.model_name: record for record in  Model.objects.all()}

            for row in reader:
                model_name = row['model_name']
                manufacturer = row.get('manufacturer', '')
                model_type = row.get('model_type', '')

                if model_name not in existing_records:
                    new_record =  Model(
                        model_name=model_name,
                        manufacturer=manufacturer,
                        model_type=model_type
                    )
                    new_records.append(new_record)

            try:
                with transaction.atomic():
                    if new_records:
                        Model.objects.bulk_create(new_records)
                messages.success(request, "CSV file imported successfully")
            except Exception as e:
                messages.error(request, f"Error importing CSV file: {e}")

            return redirect('admin:assets_model_changelist')
    else:
        form = CSVUploadForm()

    context = {
        'form': form,
    }
    return render(request, "admin/upload_csv.html", context)

def success(request):
    return render(request, 'admin/success.html')