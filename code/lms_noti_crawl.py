import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

lms_noti_result = pd.DataFrame(columns=['title', 'content', 'date', 'office'])

session = requests.session()

login_url = "https://lms.kau.ac.kr/login/index.php"
data = {
    "username": "2019125051",
    "password": "Qktpgtpgti1!"
}

response = session.post(login_url, data=data)
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

lms_noti_result.to_csv("C:/Users/jerry/셓셓/소프트/2023-1/산학프로젝트/lms_noti_result.csv")