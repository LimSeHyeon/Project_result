import json
import boto3
import time
import os
import pymysql

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]

api_client = boto3.client('apigatewaymanagementapi', endpoint_url="https://b3gzygvo6b.execute-api.ap-northeast-2.amazonaws.com/production")

def lambda_handler(event, context):
    route_key = event["requestContext"]["routeKey"]
    connect_id = event["requestContext"]["connectionId"]
    
    if route_key == 'sendmessage':
        getData = json.loads(event['body'].replace("'",'"'))
        client = getData['client']
        userid = getData['userid']
        
        stepfunctions_client = boto3.client('stepfunctions')
        workflow_name = 'Hang_GPT'
        
        input_data = {
            "input": {
                "idx" : [0,1,2],
                "client" : client,
                "userid" : userid,
                "connect_id" : connect_id
            }   
        }
        
        #Step function 실행
        response = stepfunctions_client.start_execution(
            stateMachineArn='arn:aws:states:ap-northeast-2:387015699163:stateMachine:Hang_GPT',
            input=json.dumps(input_data)
        )
        
        return {
            'statusCode': 200
        }
        
    else:
        pass
        
    return {
        'statusCode': 200
    }