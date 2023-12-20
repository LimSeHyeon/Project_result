import os
import pymysql
import json

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]

# mysql에 접속하는 코드
connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)

def lambda_handler(event, context):
    if event["httpMethod"] == "POST":
        cursor = connect.cursor()
        userid = event['body']['userid']
        sender = event['body']['sender']
        content = event['body']['content']
        sql = "INSERT INTO chatdata (userid, sender, content) VALUES (%s, %s, %s)"
        val = (userid, sender, content)
        cursor.execute(sql, val)
        connect.commit()
        
        return {
            "statusCode":200,
            "Content-Type": "application/json",
            "body":json.dumps("SUCCESS")
        }
        
    elif event["httpMethod"] == "GET":
        cursor = connect.cursor()
        userid=event['queryStringParameters']['userid']
        sql = f"SELECT * FROM chatdata WHERE userid='{userid}'"
        cursor.execute(sql)
        rows = cursor.fetchall()

        return {
            "statusCode": 200,
            "body":json.dumps(rows)
        }