import requests
import urllib
from bs4 import BeautifulSoup
import os

domain = "http://203.252.166.206:5000"

def get_weather():
    url = domain + "/get_weather"
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.findChildren()

    ret = {}
    for i in link:
        ret[i.name] = i.text
    return ret

def get_news(category):
    url = domain + "/get_news?category=" + category
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find_all("news")

    ret = []

    for i in link:
        ret.append([i.title.text, i.content.text])

    return ret

def get_location():
    location = ""

    req = requests.get("http://ipconfig.kr")
    html = req.text
    html = html[html.find("IP address : "):].splitlines()[0]
    html = html[html.find(": ")+2:]
    html = html[html.find("red> ")+5:html.find("</font>")]
    #print(html)

    info = {'query' : html,       # target ip (my ip)
            'ip' : html}       # my ip

    with requests.Session() as s:
        req = s.post('https://후이즈검색.한국/kor.whois.jsc', data = info)
        html = req.text
        html = html[html.rfind("[ 네트워크 할당 정보 ]"):]
        html = html[:html.find("우편번호")]
        html = html.splitlines()[-1]
        html = html[html.find(": ")+2:]
        html = html.split(" ")
        for i in html:
            location = location + i + " "
            if i.endswith("구"):
                break

    return location

def get_schedule():
    schedules = []
    schedules.append(["12:00", "족발먹기"])
    schedules.append(["14:20", "곱창먹기"])
    schedules.append(["15:00", "학교가기"])

    return schedules

def upload_picture(file):
    url = domain + "/face_upload"
    files = {'file':open(file, 'rb')}
    r = requests.post(url, files=files)


def get_mp3_file():
    url = domain + "/download_mp3_file/"
    fileName = 'a.mp3'
    path = 'C:/Users/jaewook/Desktop/'
    url_request = urllib.request.Request(url+fileName)
    url_connect = urllib.request.urlopen(url_request)
    with open(path + fileName, 'wb') as f:
        while True:
            buffer = url_connect.read(1024)
            if not buffer: break
            data_write = f.write(buffer)
    url_connect.close()

if __name__ == "__main__":
    loc = get_location()
    print(loc)