#coding:utf-8
from urllib import request
import re
from bs4 import BeautifulSoup


url = 'http://trade.500.com/jczq/'
req = request.urlopen(url)
con = req.read().decode('gbk')
rs = re.findall(r'<tr zid=.*?</tr>', con, re.S)
list1 = []
for item in rs:
    soup = BeautifulSoup(item, 'html5lib')
    league = soup.span.a.string
    dict1 = {}
    dict1['league'] = league
    dict1['time'] = soup.span.span.attrs['title']
    c = soup.span.select('a[title]')
    dict1['host_team'] = c[0].string
    dict1['away_team'] = c[1].string
    list1.append(dict1)

for i in list1:
    print ('%s %s %s vs %s \n' %(i['time'], i['league'], i['host_team'], i['away_team'])) 
    #print (i)
    
    