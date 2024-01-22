import base64
from django.conf import settings
import boto3
import logging
from django.http import JsonResponse
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import json

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