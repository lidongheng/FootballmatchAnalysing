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