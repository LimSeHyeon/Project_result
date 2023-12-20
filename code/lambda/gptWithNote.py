import os
import json
import openai
import requests
import pymysql
import botocore.exceptions

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]
gpt_key = os.environ["GPT_KEY"]
api_key = os.environ["API_KEY"]

def lambda_handler(event, context):
    # TODO implement
    num = int(event['num'])
    noteid = event['keywordResult']['noteid'][num]
    notename = event['keywordResult']['notename'][num]
    client = event['keywordResult']['client']
    userid = event['keywordResult']['userid']
    connect_id = event['keywordResult']['connect_id']
    try:
        connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
        cursor = connect.cursor()
        sql = f"SELECT content FROM {notename} WHERE `index`=%s"
        val = (noteid,)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        note = [row[0] for row in rows]
        openai.api_key = gpt_key
        contents = []
        contents.append(f"{note}")
        contents.append(f"{client}의 답을 위의 내용에서 찾아주고 위의 내용에 대한 요약을줘. 위의 내용에서 답을 찾을수 없으면 '대답을 찾을 수 없습니다.'라고 해줘")
        messages = [{"role": "user", "content": f"{contents}"}]
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        assistant_content = completion.choices[0].message["content"].strip()
        
        return {
            'statusCode': 200,
            'userid' : userid,
            'client' : client,
            'notename': notename,
            'noteid': noteid,
            'connect_id': connect_id,
            'answer' : assistant_content
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'errorType':"APIError",
            'error': str(e),
            'connect_id': connect_id
        }