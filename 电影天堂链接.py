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