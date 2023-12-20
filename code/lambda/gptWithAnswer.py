import os
import pymysql
import json
import openai
import requests
import botocore.exceptions
import boto3


host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]

gpt_key = os.environ["GPT_KEY"]
api_key = os.environ["API_KEY"]

# websocket
api_client = boto3.client('apigatewaymanagementapi', endpoint_url="https://b3gzygvo6b.execute-api.ap-northeast-2.amazonaws.com/production")

def lambda_handler(event, context):
    note = ""
    nameList = []
    indexList = []
    
    input_data = list(event['results'].values())
    connect_id = input_data[0]['connect_id']
    try:
        for result in input_data:
            if result['statusCode'] != 200:
                raise Exception(result['error'])
            note += result['answer']
            nameList.append(result['notename'])
            indexList.append(result['noteid'])
            
            userid = result['userid']
            question = result['client']
        
        contents = []
        openai.api_key = gpt_key
        contents.append(f"{note}")
        contents.append(f"{question}에 대한 답을 위의 내용에서 찾아줘. 위의 내용에서 답을 찾을수 없으면 '대답을 찾을 수 없습니다.'라고 해줘")
        messages = [{"role": "user", "content": f"{contents}"}]
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        assistant_content = completion.choices[0].message["content"].strip()
        
        similarity = []
        for i in range(2,-1,-1):
            similarity.append({
                'id': int(2-i),
                'noteName': nameList[i],
                'noteIdx': indexList[i]
            })
        
        connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
        cursor = connect.cursor()
        sender = "gpt"
        sql = "INSERT INTO chatdata (userid, sender, content, similarity) VALUES (%s, %s, %s, %s)"
        val = (userid, sender, assistant_content, json.dumps(similarity, ensure_ascii=False))
        cursor.execute(sql, val)
        connect.commit()
        
        return_value = {
            "isSuccess": True,
            "code": 200,
            "message": "OK",
            "result": {
                "similarity": similarity,
                "content": assistant_content
            }
        }
        
        response = api_client.post_to_connection(Data=json.dumps(return_value, ensure_ascii=False), ConnectionId=connect_id)
        
        return {
            'statusCode': 200
        }
    
   
    except Exception as e:
        return_value = {
            "isSuccess": False,
            "code": 500,
            "message": str(e)
        }

        response = api_client.post_to_connection(Data=json.dumps(return_value, ensure_ascii=False), ConnectionId=connect_id)
        
        return {
            'statusCode': 200
        }
        
    return {
        "statusCode": 200
    }