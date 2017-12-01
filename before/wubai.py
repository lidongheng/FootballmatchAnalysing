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
    item = '<table>'+item+'</table>'
    soup = BeautifulSoup(item, 'html5lib')
    tr = soup.find_all('tr')[0]
    tds = tr.find_all('td')
    list1.append({
        'number': tds[0].a.contents[0],
        'league': tds[1].text,
        'time': tds[2].span.text,
        'host_team': tds[3].a.contents[0],
        'away_team': tds[5].a.contents[0],
        'analyse': tds[8].a.attrs['href'],
    })

for i in list1:
    print ('%s %s %s %s vs %s \n %s \n' %(i['number'], i['time'], i['league'], i['host_team'], i['away_team'], i['analyse'])) 
    #print (i)

    
    