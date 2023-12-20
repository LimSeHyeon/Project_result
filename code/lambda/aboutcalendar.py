import os
import pymysql
import json

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]

def lambda_handler(event, context):
    # mysql에 접속하는 코드
    connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
    
    if event["httpMethod"] == "POST":
        cursor = connect.cursor()
        userid = event['body']['userid']
        year = event['body']['year']
        month = event['body']['month']
        date = event['body']['date']
        time = event['body']['time']
        content = event['body']['content']
        sql = "INSERT INTO calendardata (userid, year, month, date, time, content) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (userid, year, month, date, time, content)
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
        year=event['queryStringParameters']['year']
        month=event['queryStringParameters']['month']
        sql = f"SELECT * FROM calendardata WHERE (userid='{userid}' OR userid='{userid}_lms' OR userid='common') AND year='{year}' AND month='{month}'"
            
        cursor.execute(sql)
        rows = cursor.fetchall()
        content = []
        for r in rows:
            content.append({
                "id": r[0],
                "year": int(r[2]),
                "month": int(r[3]),
                "day": int(r[4]),
                "time": r[5],
                "content": r[6]
            })
            
        result = {
            "isSuccess": True,
            "code": 200,
            "message": "OK",
            "userID": userid,
            "result": content
        }
            
        return {
            "statusCode": 200,
            "body":json.dumps(result)
        }
        
    elif event["httpMethod"] == "DELETE":
        cursor = connect.cursor()
        userid = event['body']['userid']
        year = event['body']['year']
        month = event['body']['month']
        date = event['body']['date']
        time = event['body']['time']
        content = event['body']['content']
        sql = 'DELETE FROM calendardata WHERE userid=%s AND year=%s AND month=%s AND date=%s AND time=%s AND content=%s'
        val = (userid, year, month, date, time, content)
        cursor.execute(sql, val)
        connect.commit()

        return {
            "statusCode": 200,
            "body":json.dumps('SUCCESS_DELETE')
        }