import json
import os
import pymysql

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]

def lambda_handler(event, context):
    
    connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
    cursor = connect.cursor()
    
    id = event['queryStringParameters']['id']
    pw = event['queryStringParameters']['pw']
    
    result = ""
    sql = f"SELECT id from userdata WHERE id='{id}'"
    cursor.execute(sql)
    info = cursor.fetchall()
    if len(info)==0:
        result = "해당하는 아이디가 없습니다."
        return {
            'statusCode': 401,
            'body': json.dumps(result)
        }
        

    sql = f"SELECT psword FROM userdata WHERE id='{id}'"
    cursor.execute(sql)
    pw_check = cursor.fetchall()
    pw_check = pw_check[0][0]
    if pw == pw_check:
        statusCode = 200
        result = "로그인 성공!"
    else:
        statusCode = 401
        result = "비밀번호가 틀렸습니다."
    return {
        'statusCode': statusCode,
        'body': json.dumps(result)
    }