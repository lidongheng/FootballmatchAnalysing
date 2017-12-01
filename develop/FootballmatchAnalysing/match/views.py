#coding:utf-8
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
import urllib
import re
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    url = 'http://trade.500.com/jczq/'
    req = urllib.request.urlopen(url)
    con = req.read().decode('gbk')
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
    t = get_template('match/index.html')
    html = t.render(Context({'list': list1}))
    return HttpResponse(html)
