import os
import pymysql
import json
import openai
import requests

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db = os.environ["DB_NAME"]
gpt_key = os.environ["GPT_KEY"]
api_key = os.environ["API_KEY"]


def lambda_handler(event, context):
    noteid = event['body']['noteid']
    notename = event['body']['notename']
    userid = event['body']['userid']
    '''
    connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
    cursor = connect.cursor()
    sql = f"SELECT content FROM chatdata WHERE userid = '{user}' AND sender='user' ORDER BY idx DESC LIMIT 1"
    cursor.execute(sql)
    rows = cursor.fetchall()
    question = [rows[0] for row in rows]
    #result = result[0][0]
    
    '''
    #DB에서 사용자 질문 받아오기
    url = f"https://c5f2kve495.execute-api.ap-northeast-2.amazonaws.com/230507/chatdata?mode=2&user={userid}"
    response = requests.get(url)
    question = response.json()
    #return question
    
    
    notecontent=[]
    
    # 공지 내용 가져오기
    for i in range(len(noteid)):
        url = f"https://c5f2kve495.execute-api.ap-northeast-2.amazonaws.com/230507/get1note?mode=2&notename={notename[i]}&noteid={noteid[i]}"
        headers = {
        "Authorization": "Bearer api_key",
        "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        notecontent.append(response.json())

    #return content
    openai.api_key = gpt_key
    res=[]
    for note in notecontent:
        contents = []
        contents.append(f"{note}요약해줘")
        contents.append(f"위의 내용 요약과 {question}의 답을 함께 대답해줘. 답을 찾을 수 없으면 '답을 찾을 수 없어요. 다시 질문해 주시겠어요?'라고 물어봐줘")
        messages = [{"role": "user", "content": f"{contents}"}]
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        assistant_content = completion.choices[0].message["content"].strip()
        res.append(assistant_content)
    
    res.append(f"{question}의 답을 위의 내용에서 찾아 대답해줘.답을 찾을 수 없으면 '답을 찾을 수 없어요. 다시 질문해 주시겠어요?'라고 물어봐줘")
    messages = [{"role": "user", "content": f"{contents}"}]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    assistant_content = completion.choices[0].message["content"].strip()
    
    result = {
        "isSuccess": True,
        "code": 200,
        "message": "OK",
        "result": json.dumps(assistant_content, ensure_ascii=False)
    }


    
    # DB에 GPT 응답 추가하기
    # mysql에 접속하는 코드
    connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db)
    cursor = connect.cursor()
    sender = "gpt"
    sql = "INSERT INTO chatdata (userid, sender, content) VALUES (%s, %s, %s)"
    val = (userid, sender, assistant_content)
    cursor.execute(sql, val)
    connect.commit()
    
    '''
    url = "https://c5f2kve495.execute-api.ap-northeast-2.amazonaws.com/230507/chatdata"
    data = {
        "userid": f"{userid}",
        "sender":"gpt",
        "content": f"{result['result']}"
    }
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        clear = "Clear"
    else:
        clear = "Fail. Try Again"
    '''
    
    return {
        "note" : assistant_content
    }