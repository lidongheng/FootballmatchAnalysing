#coding:utf-8
from urllib import request
import re
from bs4 import BeautifulSoup

url = 'http://www.okooo.com/soccer/team/6/players/'
hds = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
    "Accept-Language": "zh-CN,zh;q=0.8", 
    "Cache-Control": "no-cache", 
    "Connection": "keep-alive", 
    "Host": "www.okooo.com", 
    "Upgrade-Insecure-Requests": "1", 
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}

reqhd = request.Request(url, headers = hds)
req = request.urlopen(reqhd)
con = req.read().decode('gbk')
rs = re.findall(r'<table.*?</table>', con, re.S)
soup = BeautifulSoup(rs[0], 'html5lib')
data_list = []  # 结构: [dict1, dict2, ...], dict结构{'船名': ship_name, '航次': voyage, '提单号': bill_num, '作业码头': wharf}
for idx, tr in enumerate(soup.find_all('tr')):
    if idx != 0:
        tds = tr.find_all('td')
        data_list.append({
            '号码': tds[0].contents[0],
            '球员': tds[1].a.contents[0],
            '位置': tds[2].contents[0],
            '出场': tds[3].contents[0],
            '首发': tds[4].contents[0],
            '替补': tds[5].contents[0],
            '出场时间': tds[6].contents[0],
            '进球': tds[7].contents[0],
            '助攻': tds[8].contents[0],
            '黄牌': tds[9].contents[0],
            '红牌': tds[10].contents[0],
        })
print(data_list)