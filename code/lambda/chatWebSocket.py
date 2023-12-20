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

def wait_for_execution_completion(stepfunctions_client, execution_arn):
    while True:
        response = stepfunctions_client.describe_execution(
            executionArn=execution_arn
        )
        status = response['status']
        
        if status in ['SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED']:
            output =  json.loads(response['output'])
            answer = output['finalAnswer']
            if answer['statusCode'] != 200:
                result = {
                    "statusCode" : answer['statusCode'],
                    "errorType": answer['errorType'],
                    "error": answer['error']
                }
                return result
            notename = answer['notename']
            noteid = answer['noteid']
            userid = answer['userid']
            similarity = str([f"{notename[2]}-{noteid[2]}", f"{notename[1]}-{noteid[1]}",  f"{notename[0]}-{noteid[0]}"])
            content = answer['content']
            result = {
                "similarity": similarity,
                "content": content
            }
            
            connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
            cursor = connect.cursor()
            sender = "gpt"
            sql = "INSERT INTO chatdata (userid, sender, content, similarity) VALUES (%s, %s, %s, %s)"
            val = (userid, sender, content, similarity)
            cursor.execute(sql, val)
            connect.commit()
            
            return result
            
        time.sleep(1)

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
    
        #실행된 Step Functions의 실행 ID 가져오기
        execution_arn = response['executionArn']
        
        # Step Functions 실행이 완료될 때까지 대기
        result = wait_for_execution_completion(stepfunctions_client, execution_arn)
        
        return_value = {}
        if 'statusCode' in result:
            return_value = {
                "isSuccess": False,
                "code": result['statusCode'],
                "message": result['error']
            }
        else:
            return_value = {
                "isSuccess": True,
                "code": 200,
                "message": "OK",
                "result": result
            }
            
        response = api_client.post_to_connection(Data=json.dumps(return_value, ensure_ascii=False), ConnectionId=connect_id)
        return {
            'statusCode': 200,
        }
        
    else:
        pass
        
    return {
        'statusCode': 200
    }

