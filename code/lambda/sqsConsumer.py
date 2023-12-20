import json
import boto3
import os
import pymysql

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]


def lambda_handler(event, context):
    # SQS 대기열로부터 메시지 추출
    sqs_records = event['Records']
    
    for record in sqs_records:
        # 메시지 데이터 추출
        message_body = json.loads(record['body'])
        client = message_body['client']
        userid = message_body['userid']
        
        
    
    #queue_url = "https://sqs.ap-northeast-2.amazonaws.com/387015699163/gptQueue"
    
    #sqs_client = boto3.client('sqs', region_name='ap-northeast-2')
    '''
    # SQS 메시지 조회
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        AttributeNames=[
            'All'
        ]
    )
    
    if 'Messages' in response:
        print("yes")
        messages = response['Messages']
        for message in messages:
            print(json.dumps(message))
    else:
        print("no")
    '''
    
    '''
    #람다 실행
    
    function_name = "sqsConsumer"
    
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke_async(
        FunctionName = function_name,
        InvokeArgs=json.dumps(input_data)
    )'''
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
