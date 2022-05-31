import json
import os
import pprint
import profile

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

def format_comparison_data(rekog_response_list):
    formated_data = []
    for response in rekog_response_list:
        face_data = response["FaceMatches"][0]
        profile = dict(
            name=face_data["Face"]["ExternalImageId"],
            similarity=round(face_data["Similarity"], 2)
        )
        formated_data.append(profile)
    return formated_data

def publish_json_data(data):
    file = s3.Object("image-recognition-alura-website", "data.json")
    file.put(Body=json.dumps(data))

faces = recog_faces(rekog_client=rekognition, bucket_name=BUCKET_NAME)
faces_id = [face_data["Face"]["FaceId"] for face_data in faces["FaceRecords"]]

compared_faces_response = compare_faces(rekog_client=rekognition, faces_id=faces_id)
formated_face_data = format_comparison_data(compared_faces_response)
pprint.pprint(formated_face_data)

publish_json_data(formated_face_data)
