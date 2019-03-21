# Python爬虫

------

> *请求网站并提取数据的自动化程序*

## Python库

urllib

re

requests

selenium

chromedriver

phantomjs

lxml

beautifulsoup

pyquery

pymysql

pymongo

redis

flask

django

jupyter

## 爬虫基本原理

### 基本流程：

1. 发起请求（Request）
2. 获取响应内容（Response）
3. 解析内容
4. 保存数据

### Request包含：

1. 请求方式：GET & POST

2. URL
3. 请求头    Request Headers
4. 请求体（POST需要 Form Data表单数据）

### Response包含：

1.响应状态    Status Code

2.响应头        Response Headers

3.响应体

## 爬虫能抓取啥数据？

1. 网页文本
2. 图片 (二进制流)

3. 视频
4. 其他

## 解析网页

1. 直接处理
2. Json解析
3. 正则表达式
4. Beautiful Soup
5. PyQuery
6. XPath

## JavaScript渲染问题

1. 分析Ajax请求
2. selenium、webdriver  （Elements 和 Network_Response里面的东西是不同的，很多信息会藏在JS里面）
3. splash库

## 保存数据

1. 文本
2. 关系型数据库
3. key-value数据库 ——Redis、MongoDB
4. 二进制文件

## Urllib库

1. urllib.request	请求模块
2. urllib.error             异常处理模块
3. urllib.parse            url解析模块
4. urllib.robotparse  

https://docs.python.org/3/library/urllib.html

## Requests库(*)

http://docs.python-requests.org/zh_CN/latest/user/quickstart.html



## 正则表达式(*)

- 《正则表达式必知必会》

- re模块：

  - re.compile
  - re.search
  - re.match
  - re.findall
  - re.split
  - re.sub

  http://www.runoob.com/python/python-reg-expressions.html

## Beautiful Soup

https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

## CSS选择器(*)

http://www.w3school.com.cn/cssref/css_selectors.ASP

## PyQuery库(*)

http://www.w3school.com.cn/cssref/css_selectors.ASP

## Selenium(*)

https://selenium-python-zh.readthedocs.io/en/latest/getting-started.html

## Proxy代理池

做成接口，外部调用

## Cookie池

做成接口，外部调用

## PySpider框架

牛逼啊！

## Scrapy框架



------

# 案例

## 1、电影天堂链接爬取

```python
# coding=utf-8
import re
import requests
import xlsxwriter
from bs4 import BeautifulSoup

def getHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
        page.encoding = 'gbk'
        html = page.text
        return html
    except:
        return ""

def getMovie(html):
    allmovie = []       #电影名称
    movieurl = []       #电影链接url地址
    ftpurl = []         #获取下载ftp地址
    soup = BeautifulSoup(html, 'html.parser')
    url_info = soup.find_all('a', class_='ulink')
    for url in url_info:
        movie = url.get_text()
        movie = movie.split('《')[1]
        movie = movie.split('》')[0]
        allmovie.append(movie)
        reurl = 'http://www.dytt8.net'+url.get('href')
        movieurl.append(reurl)
    for url in movieurl:
        try:
            html = getHtml(url)
            reg = r'href="(ftp:.+?)"'
            imgre = re.compile(reg)
            imglist, *_ = re.findall(imgre, html)
            ftpurl.append(imglist)
        except:
            print('访问异常，无法获取下载地址')
            ftpurl.append('')
    return allmovie, ftpurl

if __name__ == '__main__':
    workbook = xlsxwriter.Workbook(r'D:\Data\爬虫\电影资源.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for i in range(10):
        print('正在访问第{}页'.format(i+1))
        url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_'+str(i+1)+'.html'
        html = getHtml(url)
        if not html:
            print('访问异常，略过')
            continue
        movie, ftp = getMovie(html)
        for item in zip(movie, ftp):
            worksheet.write(row, 0, item[0])
            worksheet.write(row, 4, item[1])
            row += 1
    workbook.close()
    print("下载完成！")
```

## 2、百度贴吧图片

```python
# coding=utf-8
import re
import requests

def getHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    try:
        page = requests.get(url, headers = headers)
        page.encoding = 'utf-8'
        html = page.text
        return html
    except:
        return ''

def getImg(html):
    reg = r'src="([.*\S]*\.jpg)" pic_ext="jpeg"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    return imglist

if __name__ == '__main__':
    url = "http://tieba.baidu.com/p/3205263090"
    html = getHtml(url)
    imgList = getImg(html)
    imgCount = 0
    for imgPath in imgList:
        f = open('D://Data/爬虫/百度贴吧图/'+str(imgCount)+'.jpg', 'wb')
        f.write(requests.get(imgPath).content)
        f.close()
        imgCount += 1
    print('抓取完成')
```

## 3、虎嗅新闻

```python
# coding=utf-8
import requests
from bs4 import BeautifulSoup
import chardet
import xlsxwriter

def getHtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    try:
        page = requests.get(url, headers = headers)
        page.encoding = 'utf-8'
        html = page.text
        return html
    except:
        return '没访问上虎嗅新闻'

def getInfo(html, url):
    titles = []
    hrefs = []
    imgurls = []
    soup = BeautifulSoup(html, 'html.parser')
    alllist = soup.find_all('div', class_='mod-b mod-art clearfix ')
    for news in alllist:
        try:
            href = url + news.find_all('a', class_='transition')[0]['href']
        except:
            href = '链接不存在'
        try:
            title = news.find_all('img')[0]['alt']
        except:
            title = '标题不存在'
        try:
            imgurl = news.find_all('img')[0]['data-original']
        except:
            imgurl = '图片不存在'
        hrefs.append(href)
        titles.append(title)
        imgurls.append(imgurl)
    return (titles,hrefs,imgurls)

if __name__ == '__main__':
    workbook = xlsxwriter.Workbook(r'D:\Data\爬虫\虎嗅新闻.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    url = 'https://www.huxiu.com'
    html = getHtml(url)
    title, href, imgurl = getInfo(html, url)
    for item in zip(title, href, imgurl):
        worksheet.write(row, 0, item[0])
        worksheet.write(row, 4, item[1])
        worksheet.write(row, 10, item[2])
        row += 1
    workbook.close()
    print("爬取完成")
```

## 4、豆瓣图书

被封了ip，试一试proxy，实现根据tag爬书，会翻页

还好，第二天解封了

```
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
```



## 5、猫眼电影Top100

```
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
```

## 6、今日头条图文爬取

源数据里面的json格式有点问题，需要解决
