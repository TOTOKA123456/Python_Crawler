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