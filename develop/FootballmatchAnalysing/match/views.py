#coding:utf-8
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from urllib import request
import re
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
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
        dict1['number'] = soup.a.text
        dict1['time'] = soup.span.span.attrs['title']
        dict1['time'] = dict1['time'][-5:]
        c = soup.span.select('a[title]')
        dict1['host_team'] = c[0].string
        dict1['away_team'] = c[1].string
        list1.append(dict1)
    t = get_template('match/index.html')
    html = t.render(Context({'list': list1}))
    return HttpResponse(html)
