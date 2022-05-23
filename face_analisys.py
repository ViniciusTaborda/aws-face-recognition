import os
import pprint

import boto3

os.environ["AWS_PROFILE"] = "personal"

s3 = boto3.resource("s3")
rekognition = boto3.client("rekognition")

BUCKET_NAME = "image-recognition-alura"

def recog_faces(rekog_client, bucket_name):
    regognized_faces = rekog_client.index_faces(
            CollectionId="faces",
            DetectionAttributes=["DEFAULT"],
            ExternalImageId="temp_image",
            Image={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": "_analysis.jpg",
                }
            }
        )
    return regognized_faces

def compare_faces(rekog_client, faces_id):
    result = []
    for id in faces_id:
        result.append(rekog_client.search_faces(
            CollectionId="faces",
            FaceId=id,
            FaceMatchThreshold=80,
            MaxFaces=10,
        ))
    return result


faces = recog_faces(rekog_client=rekognition, bucket_name=BUCKET_NAME)
faces_id = [face_data["Face"]["FaceId"] for face_data in faces["FaceRecords"]]

compared_faces_response = compare_faces(rekog_client=rekognition, faces_id=faces_id)
pprint.pprint(compared_faces_response)
