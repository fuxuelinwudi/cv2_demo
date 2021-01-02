# -*- coding: utf-8 -*-
import re
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import pandas as pd


# 主函数
def main(url):
    datalist = getData(url)
    savepath = "天涯评论.xls"
    saveData(datalist, savepath)   #保存到excel里


#  规则
findContent = re.compile(r'<div class="bbs-content">(.*)</div>',re.S)
findTitle =  re.compile(r'<span style=".*?">(.*?)</span>',re.S)


# 爬取网页
def getData(url):
    datalist = []
    datalist1 = []
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="bbs-content"):
        data = []
        item = str(item)

        content = re.findall(findContent, item)
        content = [x.replace("<br/>", "\n") for x in content]
        data.append(content)

        datalist.append(data)


    for item1 in soup.find_all('span',class_="s_title"):
        data1 = []
        item1 = str(item1)

        title = re.findall(findTitle, item1)
        data1.append(title)

        datalist1.append(data1)

    datalist.append(datalist1)
    return datalist

# 得到一个指定url的网页内容
def askURL(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据
def saveData(datalist,savepath):
    # 使用pandas保存
    df = pd.DataFrame({'评论内容': datalist})
    # 保存到本地excel
    df.to_excel(savepath, index=True)



