from django.conf import settings
from django.shortcuts import render
from .models import WorkOrder

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import boto3
import io
from PIL import Image


# Create your views here.
def display_photo(request, photo_id):
    photo = get_object_or_404(WorkOrder, pk=photo_id)

    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)

    obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=photo.photo_key)

    image = Image.open(io.BytesIO(obj['Body'].read()))
    image.show()

    return HttpResponse("Photo displayed.")