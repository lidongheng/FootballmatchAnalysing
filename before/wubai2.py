#coding:utf-8
from urllib import request
import re
from bs4 import BeautifulSoup
import gzip

url = 'http://odds.500.com/fenxi/shuju-699400.shtml'
hds = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
    "Accept-Language": "zh-CN,zh;q=0.8", 
    "Accept-encoding": "gzip",
    "Cache-Control": "no-cache", 
    "Connection": "keep-alive", 
    "Host": "odds.500.com", 
    "Upgrade-Insecure-Requests": "1", 
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
reqhd = request.Request(url, headers = hds)
req = request.urlopen(reqhd)
doc = req.read()
con = gzip.decompress(doc).decode('gbk')
soup = BeautifulSoup(con, 'html5lib')
odds_content = soup.select('.odds_content')
odds_content[0].select('.M_sub_title')[0].select('.team_name')[0].text
odds_content[0].select('.M_sub_title')[0].select('.team_name')[1].text
#jifenbang
data_list1 = []
for idx, tr in enumerate(odds_content[0].select('.team_a')[0].find_all('tr')):
    if idx != 0:
        tds = tr.find_all('td')
        data_list1.append({
            '比赛': tds[1].contents[0],
            '胜': tds[2].contents[0],
            '平': tds[3].contents[0],
            '负': tds[4].contents[0],
            '进': tds[5].contents[0],
            '失': tds[6].contents[0],
            '净': tds[7].contents[0],
            '积分': tds[8].span.contents[0],
            '排名': tds[9].contents[0],
            '胜率': tds[10].contents[0],
        })
data_list2 = []
for idx, tr in enumerate(odds_content[0].select('.team_b')[0].find_all('tr')):
    if idx != 0:
        tds = tr.find_all('td')
        data_list2.append({
            '比赛': tds[1].contents[0],
            '胜': tds[2].contents[0],
            '平': tds[3].contents[0],
            '负': tds[4].contents[0],
            '进': tds[5].contents[0],
            '失': tds[6].contents[0],
            '净': tds[7].contents[0],
            '积分': tds[8].span.contents[0],
            '排名': tds[9].contents[0],
            '胜率': tds[10].contents[0],
        })
#交战历史
odds_content[0].select('.history')[0].select('.his_info')[0].text

data_list3 = []
for idx, tr in enumerate(odds_content[0].select('.history')[0].select('.M_content')[0].find_all('tr')):
    if idx > 1:
        tds = tr.find_all('td')
        dict1 = {}
        dict1['赛事'] = tds[0].a.text
        dict1['日期'] = tds[1].contents[0]
        dict1['对阵'] = tds[2].text
        dict1['半场'] = tds[3].text
        dict1['赛果'] = tds[4].span.contents[0]
        dict1['欧赔'] = tds[5].text
        dict1['亚盘'] = tds[6].text
        if tds[7].span == None:
            dict1['盘路'] = tds[7].contents[0]
        else:
        	  dict1['盘路'] = tds[7].span.text
        if tds[8].span == None:
            dict1['大小'] = tds[8].contents[0]
        else:
        	  dict1['大小'] = tds[8].span.text
        data_list3.append(dict1)

data_list4 = []
for idx, tr in enumerate(odds_content[0].select('.record')[0].select('#team_zhanji_1')[0].select('.M_content')[0].find_all('tr')):
    if idx != 0 and idx < 12:
        tds = tr.find_all('td')
        dict1 = {}
        dict1['赛事'] = tds[0].text
        dict1['日期'] = tds[1].contents[0]
        dict1['对阵'] = tds[2].text
        dict1['盘口'] = tds[3].text
        dict1['半场'] = tds[4].text
        dict1['赛果'] = tds[5].text
        if tds[6].span == None:
            dict1['盘路'] = tds[6].contents[0]
        else:
            dict1['盘路'] = tds[6].span.text
        if tds[7].span == None:
            dict1['大小'] = tds[7].contents[0]
        else:
            dict1['大小'] = tds[7].span.text
        data_list4.append(dict1)

data_list5 = []
for idx, tr in enumerate(odds_content[0].select('.record')[0].select('#team_zhanji_0')[0].select('.M_content')[0].find_all('tr')):
    if idx != 0 and idx < 12:
        tds = tr.find_all('td')
        dict1 = {}
        dict1['赛事'] = tds[0].text
        dict1['日期'] = tds[1].contents[0]
        dict1['对阵'] = tds[2].text
        dict1['盘口'] = tds[3].text
        dict1['半场'] = tds[4].text
        dict1['赛果'] = tds[5].text
        if tds[6].span == None:
            dict1['盘路'] = tds[6].contents[0]
        else:
            dict1['盘路'] = tds[6].span.text
        if tds[7].span == None:
            dict1['大小'] = tds[7].contents[0]
        else:
            dict1['大小'] = tds[7].span.text
        data_list5.append(dict1)

odds_content[0].select('.record')[0].select('#team_zhanji_1')[0].select('.M_content')[0].select('.bottom_info')[0].p.text
odds_content[0].select('.record')[0].select('#team_zhanji_0')[0].select('.M_content')[0].select('.bottom_info')[0].p.text

data_list6 = []
for idx, tr in enumerate(odds_content[0].select('.record')[0].select('#zhanji_11')[0].select('.M_content')[0].find_all('tr')):
    if idx != 0 and idx < 12:
        tds = tr.find_all('td')
        dict1 = {}
        dict1['赛事'] = tds[0].text
        dict1['日期'] = tds[1].contents[0]
        dict1['对阵'] = tds[2].text
        dict1['盘口'] = tds[3].text
        dict1['半场'] = tds[4].text
        dict1['赛果'] = tds[5].text
        if tds[6].span == None:
            dict1['盘路'] = tds[6].contents[0]
        else:
            dict1['盘路'] = tds[6].span.text
        if tds[7].span == None:
            dict1['大小'] = tds[7].contents[0]
        else:
            dict1['大小'] = tds[7].span.text
        data_list6.append(dict1)

data_list7 = []
for idx, tr in enumerate(odds_content[0].select('.record')[0].select('#zhanji_20')[0].select('.M_content')[0].find_all('tr')):
    if idx != 0 and idx < 12:
        tds = tr.find_all('td')
        dict1 = {}
        dict1['赛事'] = tds[0].text
        dict1['日期'] = tds[1].contents[0]
        dict1['对阵'] = tds[2].text
        dict1['盘口'] = tds[3].text
        dict1['半场'] = tds[4].text
        dict1['赛果'] = tds[5].text
        if tds[6].span == None:
            dict1['盘路'] = tds[6].contents[0]
        else:
            dict1['盘路'] = tds[6].span.text
        if tds[7].span == None:
            dict1['大小'] = tds[7].contents[0]
        else:
            dict1['大小'] = tds[7].span.text
        data_list7.append(dict1)


odds_content[0].select('.record')[0].select('#zhanji_11')[0].select('.M_content')[0].select('.bottom_info')[0].p.text
odds_content[0].select('.record')[0].select('#zhanji_20')[0].select('.M_content')[0].select('.bottom_info')[0].p.text

data_list8 = []
for idx, tr in enumerate(odds_content[0].select('.integral')[0].select('.M_content')[0].select('.team_a')[0].find_all('tr')):
    if idx != 0:
        tds = tr.find_all('td')
        dict1 = {}
        dict1['赛事'] = tds[0].text
        dict1['日期'] = tds[1].contents[0]
        dict1['对阵'] = tds[2].text
        dict1['相隔'] = tds[3].text
        data_list8.append(dict1)

data_list9 = []
for idx, tr in enumerate(odds_content[0].select('.integral')[0].select('.M_content')[0].select('.team_b')[0].find_all('tr')):
    if idx != 0:
        tds = tr.find_all('td')
        dict1 = {}
        dict1['赛事'] = tds[0].text
        dict1['日期'] = tds[1].contents[0]
        dict1['对阵'] = tds[2].text
        dict1['相隔'] = tds[3].text
        data_list9.append(dict1)

        