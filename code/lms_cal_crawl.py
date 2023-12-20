import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

lms_calendar_result = pd.DataFrame(columns=['userid', 'year', 'month', 'date', 'time', 'content'])

session = requests.session()

login_url = "https://lms.kau.ac.kr/login/index.php"
about_user = {
    "username": "2021125071",
    "password": "2021125071020607"
}

response = session.post(login_url, data=about_user)

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

lms_calendar_result.to_csv("./lms_calendar_result.csv")
