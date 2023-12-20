import json
import io
import boto3

def lambda_handler(event, context):
    #s3 연결 정보 설정 설정
    s3 = boto3.resource('s3')
    bucket_name = 'hang-gpt-bucket1'
    object_key = 'puppy/puppy.jpg'
    
    obj = s3.Object(bucket_name, object_key)
    
    body = obj.get()['Body'].read()
        f.write(body)
    
    return {
        'statusCode': 200,
        'body': json.dumps('here your puppy')
    }
