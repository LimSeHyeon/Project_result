import os
import pymysql
import json


#한 페이지 목차들만 긁어오기

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]

#목록 받아오기
def lambda_handler(event, context):
    connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
    
    cursor = connect.cursor()
    mode = event['queryStringParameters']['mode']
    note_name = event['queryStringParameters']['noteName']
    
    
    if mode=='1':
        page_num = 0
        paging_count = 5
    elif mode=='2':
        page_num = int(event['queryStringParameters']['pageNum'])*20
        paging_count = 20
    
    sql = f"SELECT `index`, title, date, office FROM {note_name} ORDER BY `date` DESC LIMIT {page_num}, {paging_count}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    content = []
    for r in rows:
        content.append({"id":r[0]+1, "title":r[1], "date":r[2], "office":r[3]})
        
    result = {
        "isSuccess": True,
        "code": 200,
        "message": "OK",
        "result": content
    }

    return {
        "statusCode": 200,
        "body":json.dumps(result)
    }