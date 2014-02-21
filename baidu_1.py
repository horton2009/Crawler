# -*- coding: utf-8 -*- 
#import requests
from bs4 import  BeautifulSoup
import urllib2
import sys
import pymongo
import threading

# 通过命令行来输入抓取的页面 url
def get_url():
    try:
        return sys.argv[1]
    except :
        return "http://baike.baidu.com/link?url=4ujp8ZgllKeJ5qQJhkNqQWt2W5v1gBEhAfLAKjXcvr3UWT6B3OYHc5OUaZItxjyT"

#def get_url(keyWord):
#    url="http://baike.baidu.com/search/word?word=%s&pic=1&sug=1&enc=utf8"%(keyWord)

def change_Proxy(i):
    Proxy=['192.227.137.47:7808', '61.163.162.251:8000', '60.214.67.86:80', '60.29.43.130:9999', '58.252.56.148:9000', 
    '60.195.251.213:80', '61.133.125.186:50634', '61.136.93.38:8080', '1.192.224.66:8888', '58.53.192.218:8123',
     '58.211.195.86:8080', '58.213.114.77:8080', '58.215.184.174:8080', '58.250.87.121:81', '58.250.87.122:81', 
    '59.57.15.71:80', '60.214.67.86:8080', '59.124.2.233:80', '59.172.208.190:8080', '61.158.172.145:8080', 
    '59.148.224.190:80', '61.164.184.66:8080', '61.134.38.42:7280', '61.153.236.30:8080', '59.172.208.186:8080', 
    '61.167.49.188:8080', '61.143.61.92:52013', '61.175.223.139:3128', '61.175.223.141:3128', '60.195.251.202:80', 
    '60.223.255.141:8080', '60.223.228.2:8080', '60.5.254.168:8081', '61.134.62.119:9999', '60.216.99.222:80']
    if i>0:
        print ("---------------------------------- Change Proxy! ------------------------------------")
        j=(i-1)%35
        daili_ip=Proxy[j]
        proxy_handler = urllib2.ProxyHandler({"http" :daili_ip})  
        opener = urllib2.build_opener(proxy_handler)  

        opener.addheaders("User-Agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36")
        # 伪装成浏览器

        urllib2.install_opener(opener)
    elif i==0:
        proxy_handler = urllib2.ProxyHandler({})   # 不设置代理 
        opener = urllib2.build_opener(proxy_handler)  
        urllib2.install_opener(opener)

# 根据 url 下载并返回页面内容
def get_page(url):
    i=0
    change_Proxy(i)
    while True:
        try:
            page=urllib2.urlopen(url).read()
            break
        except urllib2.URLError, e:
            # 处理 URLError
            if hasattr(e, 'reason'):  
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
                sys.exit()

            # 处理 HTTPError
     #       elif hasattr(e, 'code'):
     #           print 'The server couldn\'t fulfill the request.'    
     #           print 'Error code: ', e.code 
     #           sys.exit()
            else:
                i=i+1
                change_Proxy(i)
    return page

# 使用BeautifulSoup 从网页内容提取并返回基本信息字典
def get_baseInfo(page):
    soup=BeautifulSoup(page)
    bi=soup.find(class_="baseInfoWrap")
    if bi:
        info={}
        for child in bi.children:
            for biIterm in child:
                biTitle=biIterm.find(class_="biTitle")
                key=unicode(biTitle.string).replace(u'\xa0',"")
                # 网页源码中空格用 &nbsp;表示，转换成 unicode 变为 u'\xa0', 与字符串中的空格不一样
                biContent=biIterm.find(class_="biContent")
                content=""
                for s in biContent.strings:
                    content+=s
                info[key]=content
        return info
    else:
        return None






# 输出基本信息字典
def print_baseInfo(info):
    for (k,v) in info.items():
        print k+" : "+v

# 保存基本信息到 mongodb 数据库
def save_baseInfo(info):
    conn=pymongo.Connection()
    db=conn.baike
    db.people.save(info)

def multiThread_test(num):
    for k in range(1000):
        url=get_url()
        page=get_page(url)
        info=get_baseInfo(page)
        # 保存后输出可能出错
        print_baseInfo(info)
        #save_baseInfo(info)
        print "-",num,"- thread" "finished %s times "%(k+1)
        print " "

def main():
    for i in range(20):
        num=i+1
        thread_new=threading.Thread(target=multiThread_test,args=(num,)) # args 参数为目标函数的参数，用
        thread_new.start()


if __name__ == '__main__':
    main()
    
