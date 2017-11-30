#coding:utf-8
from urllib import request
import re
from bs4 import BeautifulSoup

url = 'http://odds.500.com/fenxi/shuju-699400.shtml'

req = request.urlopen(url)
con = req.read().decode('gbk')
soup = BeautifulSoup(con, 'html5lib')
odds_content = soup.select('.odds_content')