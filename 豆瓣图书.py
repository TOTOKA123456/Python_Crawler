# coding=utf-8
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd
import urllib

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    img_hrefs = []
    titles = []
    book_hrefs = []
    soup = BeautifulSoup(html, 'html.parser')
    item_list = soup.find_all('li', class_='subject-item')
    for item in item_list:
        try:
            img_href = item.find_all('img')[0]['src']
        except:
            img_href = '图片不存在'
        try:
            title = item.find_all('a')[1]['title']
        except:
            title = '标题不存在'
        try:
            book_href = item.find_all('a')[1]['href']
        except:
            book_href = '图书链接不存在'
        img_hrefs.append(img_href)
        titles.append(title)
        book_hrefs.append(book_href)
    return img_hrefs, titles, book_hrefs

if __name__ == '__main__':
    data = []
    book_tags = ['台湾言情', '言情']
    for book_tag in book_tags:
        for i in range(5):
            url = 'https://book.douban.com/tag/'+urllib.parse.quote(str(book_tag))+'?start='+str(i*20)+'&type=T'
            html = get_one_page(url)
            img_href, title, book_href = parse_one_page(html)
            for item in zip(img_href, title, book_href):
                data.append(list(item))
    df = pd.DataFrame(data, columns=['img_href', 'title', 'book_href'])
    df.to_csv(r'D:\Data\爬虫\豆瓣图书.csv', index=False)
    print('爬取完成')