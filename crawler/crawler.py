import requests
from bs4 import BeautifulSoup
import re
# import HTMLParser
# import time
import sys

url = 'https://www.wikihow.com/Category:Furniture'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
# dcard_title = soup.find_all('h3', re.compile('PostEntry_title_'))
dcard_title = soup.find_all('div','thumbnail s-height s-width')
links = []
for link in dcard_title:
        link = 'https:' + [tag['href'] for tag in link.findAll('a',{'href':True})][0]
        # print(link)
        links.append(link)

wikihow_list = open('wikihow_list_Furniture.txt','w')

for i in range(len(links)):

    res = requests.get(links[i])
    print 'fecthing', links[i]
    wikihow_list.write(('fecthing '+ links[i]).encode('utf-8') + "\n")

    soup = BeautifulSoup(res.text.encode("utf-8"), 'html.parser')

    header = soup.find('div',{'id':'intro'})
    #
    title = header.h1.a.string.strip()
    wikihow_list.write(('Subject: '+title).encode('utf-8') + "\n")

    methods = soup.find_all('div', re.compile('section steps'))

    for index, method in enumerate(methods):
        # print 'Method', (index+1), method.find('span', {'class':'mw-headline'}).string
        try:
            method_header = method.find('span', {'class':'mw-headline'}).string
            wikihow_list.write(('Method '+str(index+1)+' '+method_header).encode('utf-8') + "\n")
        except Exception as e:
            method_header = ""

        step_contents_arr = method.find_all('li', 'hasimage')
        for step in step_contents_arr:
            try:
                step_num = step.find('div', {'class':'step_num'}).string
                # print 'step', step_num
                wikihow_list.write(('Step '+ step_num).encode('utf-8') + "\n")
            except Exception as e:
                step_num = ""
            try:
                step_content = step.find('div', {'class':'step'})

                wikihow_list.write(description.encode('utf-8') + "\n")
            except Exception as e:
                step_content = ""

    print i

    sys.stdout.flush()
wikihow_list.write(('total subjects: '+str(i)).encode('utf-8') + "\n")
print 'total', i
wikihow_list.close()


# print('Crawled:')
# print(dcard_title[0].text)
# for index, item in enumerate(dcard_title[:10]):
    # print("{0:2d}. {1}".format(index + 1, item.text.strip()))
    # print(item.text.strip())
