import boto3
import json
import os
import urllib3

BUCKET_NAME = os.environ['BUCKET_NAME']
http = urllib3.PoolManager()
# Get image URL from the event and download it to upload to s3
def lambda_handler(event, context):
    # download the image from the url
    download_file(event.imageUrl, event.imageName)
    # upload the image to S3
    upload_file(event.imageName, BUCKET_NAME)
    return { 
        'body': 'Uploaded image to S3',
        'statusCode': 200
    }


# Write a function to download a file from HTTP GET
def download_file(url, file_name):
    r = http.request('GET', url)
    with open(file_name, 'wb') as f:
        f.write(r.data)
    f.close()

# write a function to upload a file to S3
def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response