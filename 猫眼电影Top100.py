# coding=utf-8
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd

def get_one_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    titles = []
    hrefs = []
    stars = []
    imgs = []
    soup = BeautifulSoup(html, 'html.parser')
    dd_list = soup.find_all('dd')
    for item in dd_list:
        try:
            title = item.find_all('a')[0]['title']
        except:
            title = "标题不存在"
        try:
            href = 'https://maoyan.com'+item.find_all('a')[0]['href']
        except:
            href =  "电影主页不存在"
        try:
            star = item.find_all('p', class_='star')[0].string
            star = star.strip()[3:]
        except:
            star = "缺少主演信息"
        try:
            img = item.find_all('img', class_='board-img')[0]['data-src']
        except:
            img = "图片不存在"
        titles.append(title)
        hrefs.append(href)
        stars.append(star)
        imgs.append(img)
    return (titles,hrefs,stars,imgs)

if __name__ == '__main__':
    data = []
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset='+str(i*10)
        html = get_one_page(url)
        title, href, star, img = parse_one_page(html)
        for item in zip(title, href, star, img):
            data.append(list(item))
    df = pd.DataFrame(data, columns=['title', 'href', 'star', 'img'])
    df.to_csv(r'D:\Data\爬虫\猫眼电影.csv', index=False)
    print("爬取完成")