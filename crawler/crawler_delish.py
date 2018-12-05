# Crawl from website: https://www.delish.com/cooking/recipe-ideas/

import requests
from bs4 import BeautifulSoup
import re
import sys

url = 'https://www.delish.com/cooking/recipe-ideas/'
resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')
recipe_title = soup.find_all('div', {'class':'full-item'})
# print recipe_title[0].string
links = []
for link in recipe_title:
        link = 'https://www.delish.com' + [tag['href'] for tag in link.findAll('a',{'href':True})][0]
        # print(link)
        links.append(link)

data_list = open('recipe_delish.txt','w')

for i in range(len(links)):

    res = requests.get(links[i])
    print 'fecthing', links[i]
    data_list.write(('fecthing '+ links[i]).encode('utf-8') + "\n\n")

    soup = BeautifulSoup(res.text.encode("utf-8"), 'html.parser')

    header = soup.find('div','content-header-inner')
    #
    title = header.h1.string.strip()
    print('Subject: '+title)
    data_list.write(('Subject: '+title).encode('utf-8') + "\n\n")

    directions = soup.find('div', 'direction-lists');
    try:
        methods = directions.find_all('li')

        for index, method in enumerate(methods):
            try:
                # print 'Method', (index+1), method.string
                step = method.string
            except Exception as e1:
                step = ""

            data_list.write(step.encode('utf-8') + "\n")

        data_list.write("\n")

    except Exception as e1:
        data_list.write("None\n")


    sys.stdout.flush()
data_list.write(('total subjects: '+str(i)).encode('utf-8') + "\n")
print 'total', i
data_list.close()
