import os
import pymysql
import json
import pprint

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]



def lambda_handler(event, context):
    # mysql에 접속하는 코드
    connect = pymysql.connect(host =host, user=os.environ["DB_USERNAME"], password = password, port = 3306, db = db)
    if event['httpMethod']=="GET":
        cursor = connect.cursor()
        mode = event['queryStringParameters']['mode']
        user = event['queryStringParameters']['userID']
        page = int(event['queryStringParameters']['page'])
        
        result=[]
        
        if mode=='1':
            sql = f"SELECT * FROM chatdata WHERE userid='{user}' ORDER BY idx DESC LIMIT {page*20},20"
            cursor.execute(sql)
            rows = cursor.fetchall()
            data = []
            for r in rows:
                print(r[4])
                if r[4]==None:
                    data.append({"id":r[0], "sender":r[2], "content":r[3]})
                else:
                    data.append({"id":r[0], "sender":r[2], "content":r[3], "similarity":json.loads(r[4])})

            result = {
                "isSuccess": True,
                "code": 200,
                "message": "OK",
                "userID": user,
                "page": page,
                "data": data
            }
            return {
                "statusCode": 200,
                "body":json.dumps(result)
            }
        
        elif mode=='2':
            sql = f"SELECT content FROM chatdata WHERE userid = '{user}' AND sender='user' ORDER BY idx DESC LIMIT 1"
            cursor.execute(sql)
            rows = cursor.fetchall()
            result = [rows[0] for row in rows]
            result = result[0][0]
            return {
                "statusCode":200,
                "body":json.dumps(result)
            }  
    
    
    elif event['httpMethod']=="POST":
        userid = event['body']['userid']
        sender = event['body']['sender']
        content = event['body']['content']
        cursor = connect.cursor()
        
        sql = "INSERT INTO chatdata (userid, sender, content) VALUES (%s, %s, %s)"
        val = (userid, sender, content)
        cursor.execute(sql, val)
        connect.commit()
        
        return {
            "statusCode":200,
            "Content-Type":"application/json",
            "body":json.dumps(f"SUCCESS TO INSERT ABOUT {userid}")
        }