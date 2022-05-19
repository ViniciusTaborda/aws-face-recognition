import os

import boto3

os.environ["AWS_PROFILE"] = "personal"

s3 = boto3.resource("s3")
rekognition = boto3.client("rekognition")

BUCKET_NAME = "image-recognition-alura"

def list_bucket_images(s3_client, bucket_name):
    images = []
    bucket = s3_client.Bucket(bucket_name)
    for image in bucket.objects.all():
        images.append(image.key)
    return images

def index_collection(images_list, rekog_client, bucket_name):
    responses = []

    for image in images_list:
        response = rekog_client.index_faces(
            CollectionId="faces",
            DetectionAttributes=[],
            ExternalImageId=image[:-4],
            Image={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": image,
                }
            }
        )
        responses.append(response)

    return responses

images = list_bucket_images(s3_client=s3, bucket_name=BUCKET_NAME)
responses = index_collection(rekog_client=rekognition, bucket_name=BUCKET_NAME, images_list=images)
print(images)
print(responses)
