import requests
import url.request
from bs4 import BeautifulSoup

domain = "http://127.0.0.1:5000"

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