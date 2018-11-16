
# coding: utf-8

# In[2]:


# -*- coding:utf-8 -*-

# import urllib
# import urllib2
 
# page = 1
# url = 'https://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = { 'User-Agent' : user_agent }
# try:
#     request = urllib2.Request(url,headers = headers)
#     response = urllib2.urlopen(request)
#     print response.read()
# except urllib2.URLError, e:
#     if hasattr(e,"code"):
#         print e.code
#     if hasattr(e,"reason"):
#         print e.reason
        


# In[8]:


# import urllib.request
# page = 1
# url = 'https://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = { 'User-Agent' : user_agent }

# request = urllib.request.Request(url, headers = headers)
# response = urllib.request.urlopen(request)
# print (response.read())


# In[14]:


import requests
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/top250'
# 使用U-A伪装成浏览器发送请求
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
# 先使用requests发送网络请求从而获取网页
r = requests.get('https://movie.douban.com/top250', headers=headers)
# 使用bs4解析获取的网页
soup = BeautifulSoup(r.text, 'html.parser')
# 调用prettify()方法来使解析的HTML更加规范化
# print(soup.prettify())

movie_list = soup.find('ol', attrs={'class': 'grid_view'}) #电影列表


for movie in movie_list.find_all('li'):
    movie_name = movie.find('span', attrs={'class': 'title'})
    print(movie_name.get_text())



# In[20]:


##import 必要套件
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import time
from random import randint
import sys
from IPython.display import clear_output

##從搜尋頁面擷取店家網址（因為搜尋頁面的電話是圖片不好抓）
# links = ['http://www.ipeen.com.tw/search/all/000/1-100-0-0/?p=' + str(i+1) + 'adkw=東區&so=commno' for i in range(10)]
# links = 
page = 1
# max_page = 23
max_page = 1

dish_links=[]

while page <= max_page:
    webs = ['http://cookingtutorials.com/page/' + str(page) +'/']
    for web in webs:
        res = requests.get(web)
        soup = BeautifulSoup(res.text.encode("utf-8"))
        dish_table = soup.findAll('div',{'class':'post_header half'})
        for link in dish_table:
            link = [tag['href'] for tag in link.findAll('a',{'href':True})][0]
            print(link)
            dish_links.append(link)
    page += 1
    print("page: " + str(page))

for i in range(len(dish_links)):
    res = requests.get(dish_links[i])
    soup = BeautifulSoup(res.text.encode("utf-8"), 'html.parser')

    words = soup.find('div',{'class':'post_inner_wrapper'})
#     title = words.p.get_text()
    try:
#         title = words.find_all('p').get_text()
        titles = words.find_all('p')
        titles_len = len(title)
        for title in titles:
            print(title.get_text())
        print("-----------------------------")
        print()
    except Exception as e:
        titles = ""
        print("nothing")
 
    

