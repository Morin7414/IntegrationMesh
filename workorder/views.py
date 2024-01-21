from django.conf import settings
import boto3
import logging
from django.http import JsonResponse
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.views.decorators.http import require_GET


# Create your views here.
#def display_photo(request, photo_id):
 #   photo = get_object_or_404(WorkOrder, pk=photo_id)

  #  s3 = boto3.client('s3',
                 #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                 #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
              #        region_name=settings.AWS_S3_REGION_NAME)

   # obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=photo.photo_key)

   # image = Image.open(io.BytesIO(obj['Body'].read()))
   # image.show()

   # return HttpResponse("Photo displayed.")

@require_GET
def generate_presigned_url(request):
    image_key = request.GET.get('image_key', '')

    try:
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name='ca-central-1', config=boto3.session.Config(signature_version='s3v4')) 

        url = s3_client.generate_presigned_url('get_object',
                                              Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': f"{image_key}"},
                                              ExpiresIn=3600)  # URL expires in 1 hour
        logging.debug("BossssssGenerated URL: %s", url)

        return JsonResponse({'url': url})
    except ClientError as e:
        return JsonResponse({'error': f"Error generating URL: {e}"}, status=500)