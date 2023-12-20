import json
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import pymysql

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
db_noti = os.environ["DB_NAME_noti"]
db_cal = os.environ["DB_NAME_CAL"]

def lambda_handler(event, context):
    username = event['body']['username']
    password = event['body']['password']
    
    lms_noti_result = pd.DataFrame(columns=['title', 'content', 'date', 'office'])
    lms_calendar_result = pd.DataFrame(columns=['userid', 'year', 'month', 'date', 'time', 'content'])
    
    session = requests.session()

    login_url = "https://lms.kau.ac.kr/login/index.php"
    data = {
        "username": username,
        "password": password
    }

    response = session.post(login_url, data=data)
    
    #calendar
    soup = bs(response.text, 'html.parser')
    table = soup.select("ul.my-course-lists div.course_box > a")

    idx = 0
    for i in range(1,len(table)):
        link = table[i]['href'].split('?')[-1]
        link = "https://lms.kau.ac.kr/mod/assign/index.php?"+link
        data = session.get(link)
        data = bs(data.text, 'html.parser')
        course_name = data.select_one("div.coursename a").get_text().split("(")[0]
        data = data.select("table.generaltable tr")
        username = about_user["username"]
        for d in data[1:]:
            userid = f"{username}_table"
            content = d.select("td")
            date = content[2].get_text().split()
            time = date[1]
            date = date[0].split("-")
            year = date[0]
            month = str(int(date[1]))
            date = date[2]
            content = "["+course_name+"] "+content[1].get_text()

            lms_calendar_result.loc[idx] = [userid, year, month, date, time, content]
            idx += 1
            
    connect = pymysql.connect(host =host, user=user, password = password, port = 3306, db = db_cal)
    cursor = connect.cursor()
    for item in lms_calendar_result:
        sql = "SELECT EXISTS(SELECT 1 FROM calendardata WHERE userid=%s AND `year`=%s AND `month`=%s AND `date`=%s AND `time`=%s AND content=%s"
        val = (item[0], item[1], item[2], item[3], item[4], item[5])
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result == (1,):
            continue
        sql = "INSERT INTO calendardata ('userid', 'year', 'month', 'date', 'time', 'content') VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, val)
        connect.commit()


    #noti
    response = session.get("https://lms.kau.ac.kr/mod/ubboard/my.php?type=notice&ls=999&page=1")

    soup = bs(response.text, 'html.parser')
    table = soup.select("table.ubboard_table tr")

    for i in range(1,len(table)):
        data = table[i].select("td")

        title = data[1].get_text().replace('\t','').replace('\n','').split('\r')
        title = title[0].split("(")[0]+"] "+title[1]
        date = data[3].get_text()
        office = data[2].get_text()

        content = data[1].select_one('a')['href']
        content = session.get(content)
        content = bs(content.text, 'html.parser')
        content = content.select_one("div.content > div.text_to_html").get_text(separator="\n")

        lms_noti_result.loc[i] = [title, content, date, office]
    
    connect = pymysql.connect(host =host, use4r=user, password = password, port = 3306, db = db_noti)
    cursor = connect.cursor()
    sql = "DELETE from test1_table"
    cursor.execute(sql)
    for item in lms_noti_result:
        sql = "INSERT INTO test1_table ('title', 'content', 'date', 'office' VALUES (%s, %s, %s, %s)"
        val = (item[0], item[1], item[2], item[3])
        cursor.execute(sql, val)
    sql = "ALTER TABLE test1_table ADD COLUMN idx INT AUTO_INCREMENT PRIMARY KEY FIRST"
    cursor.execute(sql)
    sql = "ALTER TABLE test1_table ADD COLUMN notename VARCHAR(20)"
    cursor.execute(sql)
    sql = "UPDATE test1_table SET notename='test1_table'"
    cursor.execute(sql)
    
    connect.commit()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
