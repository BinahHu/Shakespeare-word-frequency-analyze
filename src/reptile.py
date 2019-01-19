import urllib3
from bs4 import BeautifulSoup
import re
import os
import json

http = urllib3.PoolManager()
root = "http://shakespeare.mit.edu/"
response = http.request('GET', root)
soup = BeautifulSoup(markup=response.data, features="html.parser")
urllist = soup.find_all('a')

for url in urllist:
    url = url['href']
    group = re.match("(.*)\/index.*", url)
    if group == None:
        continue
    playurl = root + url
    name = group[1]
    print("Handle " + name)
    if not os.path.exists("./" + name):
        os.mkdir("./" + name)
    response = http.request('GET', playurl)
    soup = BeautifulSoup(markup=response.data, features="html.parser")
    urllist = soup.find_all('a')
    for act in urllist:
        act = act['href']
        group = re.match(name + "\.(.*)\.html", act)
        if group == None:
            continue
        actid = group[1]
        print("\tAct : " + actid)
        acturl = root + name + '/' + act
        response = http.request('GET', acturl)
        soup = BeautifulSoup(markup=response.data, features="html.parser")
        f = open("./" + name + '/' + actid + '.html', 'w')
        f.write(str(soup.contents))
        f.close()