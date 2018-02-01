import boto3
import utils as util
import os

BUCKET = "test-face-rekognition"
COLLECTION = "123456789"

def search_faces_by_image(bucket, key, collection_id, threshold=80, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.search_faces_by_image(
		Image= {
                        "S3Object": {
				"Bucket": 'tmp-image-upload',
				"Name": key,
			}
		},
		CollectionId=collection_id,
		FaceMatchThreshold=threshold,
	)
	return response['FaceMatches']

def get_image_for_search(file_name):
        try :
                index = 0
                image_id = ''
                s3_client = boto3.client('s3')
                s3_client.upload_file(os.path.join('img', file_name), 'tmp-image-upload', file_name)
                items = search_faces_by_image(BUCKET,file_name, COLLECTION)        
                for result in items:
                        face = result['Face']
                        print "Matched Face ({}%)".format(result['Similarity'])
                        print "  FaceId : {}".format(face['FaceId'])
                        print "  ImageId : {}".format(face['ExternalImageId'])
                        if(index == 0) :
                                image_id = str(face['ExternalImageId'])

                        index += 1
                util.show_image(image_id)
                        
        except Exception,e:
                print str(e)
