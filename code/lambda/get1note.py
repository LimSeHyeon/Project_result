import os
import pymysql
import json


#한 페이지 목차들만 긁어오기

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]

# mysql에 접속하는 코드
connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)


def lambda_handler(event, context):
    cursor = connect.cursor()
    mode = event['queryStringParameters']['mode']       
    notename = event['queryStringParameters']['notename']
    noteid = event['queryStringParameters']['noteid']

    content = []
    isSuccess = False
    code = 0
    message = ""
    
    # 공지사항 탭에서 공지 보여줄 때
    if mode=="1":
        sql = f"SELECT title, content, date, office FROM {notename} WHERE `index`=%s"
        val = (int(noteid)-1,)
        cursor.execute(sql, val)
        raw_content = cursor.fetchall()
            
        #찾고자 하는 데이터가 없을 때
        if len(raw_content) == 0:
            result = {
                "isSuccess": False,
                "code": 404,
                "message": "Not Found"
            }
        else:
            raw_content = raw_content[0]
            content = {
                "title": raw_content[0],
                "content": raw_content[1],
                "date": raw_content[2],
                "office": raw_content[3]
            }
            result = {
                "isSuccess": True,
                "code": 200,
                "message": "OK",
                "result": content
            }
        
        
    #공지사항 내용만 불러올 때
    elif mode=="2":
        sql = f"SELECT content FROM {notename} WHERE `index`=%s"
        val = (noteid,)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        content = [row[0] for row in rows]
        
        #찾고자 하는 데이터가 없을 때
        if content == []:
            isSuccess = False
            code = 404
            message = "Not Found"
        else:
            isSuccess = True
            code = 200
            message = "OK"
            
        result = content
    
    
    
        
    
    
    return {
        "body":json.dumps(result)
        }