#coding:utf-8
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
import urllib
import re
from bs4 import BeautifulSoup
import gzip

# Create your views here.
class Basedata(object):
	def __init__(self, url, header):
        self.header = header
        self.url = url

    def wubai_connect(self):
    	reqhd = urllib.request.Request(self.url, self.header)
    	req = urllib.request.urlopen(reqhd)
    	if req.info().get('Content-Encoding') == 'gzip':
    		doc = req.read()
            con = gzip.decompress(doc).decode('gbk')
    	else:
    		con = req.read().decode('gbk')
    	return con

    def wubai_get_today_match(self, con):
        rs = re.findall(r'<tr zid=.*?</tr>', con, re.S)
        list1 = []
        for item in rs:
            item='<table>'+item+'</table>'
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
        return list1

    def __wubai_get_base_data(self, con):
    	soup = BeautifulSoup(con, 'html5lib')
        odds_content = soup.select('.odds_content')
        return odds_content

    def get_host_and_away_team(self, con):
    	odds_content = self.__wubai_get_base_data(con)
    	team = []
    	list1.append(odds_content[0].select('.M_sub_title')[0].select('.team_name')[0].text)
    	list1.append(odds_content[0].select('.M_sub_title')[0].select('.team_name')[1].text)
    	return team


def index(request):
    url = 'http://trade.500.com/jczq/'
    hds = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
            "Accept-Language": "zh-CN,zh;q=0.8", 
            "Cache-Control": "no-cache", 
            "Connection": "keep-alive", 
            "Host": "trade.500.com", 
            "Upgrade-Insecure-Requests": "1", 
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
    base_data = Basedata(url,hds)
    con = base_data.wubai_connect()
    match = base_data.wubai_get_today_match(con)
    t = get_template('match/index.html')
    html = t.render(Context({'list': match}))
    return HttpResponse(html)

def analyse(request):
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
    base_data = Basedata(url,hds)
    con = base_data.wubai_connect()
    wholedata = base_data.wubai_get_base_data(con)


