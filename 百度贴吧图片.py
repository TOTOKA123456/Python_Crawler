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