import base64
from django.conf import settings
import boto3
import logging
from django.http import JsonResponse
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.views.decorators.http import require_GET
from django.shortcuts import render
from .models import WorkOrder

from assets.models import EGM

def get_machine_details(request):
    machine_id = request.GET.get('machine_id')
    machine = EGM.objects.filter(id=machine_id).first()
    if machine:
        data = {
            'asset_number': machine.asset_number,
            'location': machine.location,
            'model': machine.model,
   
        }
        return JsonResponse(data)
    else:
        return JsonResponse({}, status=400)


def ticket_dashboard(request):
    print("Closed Tickets:")
    open_tickets = WorkOrder.objects.filter(status='EGM DOWN - Awaiting Parts').count()
    closed_tickets = WorkOrder.objects.filter(status='Troubleshooting').count()
    open_tickets = 0
    print("Open Tickets:", open_tickets)
    print("Closed Tickets:", closed_tickets)
    context = {
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
    }

    print("Open Tickets:", open_tickets)
    print("Closed Tickets:", closed_tickets)
    return render(request, 'admin/index.html', context) 

@require_GET
#@require_http_methods(["GET"])
def image_data(request, image_key):
    #image_key = request.GET.get('image_key', '')
    if not image_key:
        logging.debug("There is not image key!!!!!!!!!!!!") 
    try:
        logging.debug("MORIN")

        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name='ca-central-1', config=boto3.session.Config(signature_version='s3v4')) 

        url = s3_client.generate_presigned_url('get_object',
                                              Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': f"{image_key}"},
                                              ExpiresIn=3600)  # URL expires in 1 hour
        
           # Retrieve the image data
        image_data = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=image_key)['Body'].read()
  
        image_data_base64 = base64.b64encode(image_data).decode('utf-8')
   

        response_data = {'url': url, 'image_data': image_data_base64}
 
      #  return render(request, 'templates.html', {'json_data': {'url': url}})
      #  return HttpResponse(content=url, content_type="text/plain")
       # return JsonResponse({'url': url})
        logging.debug("OWWWWW")

      #  logging.debug("Generated URL: %s", response_data)
        return JsonResponse(response_data)
    
    except ClientError as e:
        return JsonResponse({'error': f"Error generating URL: {e}"}, status=500)
    
