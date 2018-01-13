#coding:utf-8
from urllib import request
import re
from bs4 import BeautifulSoup
import gzip

#url = 'http://caipiao.163.com/order/jczq-hunhe/#from=leftnav'
url = 'http://zx.caipiao.163.com/library/football/match.html?mId=1330076'
hds = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
    "Accept-Language": "zh-CN,zh;q=0.8", 
    "Accept-encoding": "gzi, deflate",
    "Cache-Control": "no-cache", 
    "Connection": "keep-alive", 
    "Cookie" :'_ntes_nnid=0e711f9d0121bff70ca457a034f8aa25,1512183753516; _ntes_nuid=0e711f9d0121bff70ca457a034f8aa25; JSESSIONID=abcT7RX6ceLQRgU7Mzvaw',
    "Host": "zx.caipiao.163.com", 
    "Upgrade-Insecure-Requests": "1", 
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
reqhd = request.Request(url, headers = hds)
req = request.urlopen(reqhd)
doc = req.read()
con = gzip.decompress(doc).decode('utf-8')
soup = BeautifulSoup(con, 'html5lib')
dds = soup.select('.dataBody')[1].dl.find_all('dd')
for idx, dd in enumerate(dds):
    if idx%2 == 0:
        print (dd.attrs['matchcode'][-3:])