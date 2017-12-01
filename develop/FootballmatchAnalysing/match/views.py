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
        reqhd = urllib.request.Request(self.url, headers = self.header)
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

    def wubai_get_base_data(self, con):
        soup = BeautifulSoup(con, 'html5lib')
        odds_content = soup.select('.odds_content')
        return odds_content

    def wubai_get_host_and_away_team(self, odds_content):
        team = []
        list1.append(odds_content[0].select('.M_sub_title')[0].select('.team_name')[0].text)
        list1.append(odds_content[0].select('.M_sub_title')[0].select('.team_name')[1].text)
        return team

    def wubai_get_league_table(self,con,odds_content):
        league_table = []
        for idx, tr in enumerate(odds_content[0].select(team)[0].find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                league_table.append({
                    'match': tds[1].contents[0],
                    'win': tds[2].contents[0],
                    'tie': tds[3].contents[0],
                    'defeat': tds[4].contents[0],
                    'goal': tds[5].contents[0],
                    'lose': tds[6].contents[0],
                    'diff': tds[7].contents[0],
                    'point': tds[8].span.contents[0],
                   'rank': tds[9].contents[0],
                    'win_percent': tds[10].contents[0],
                })
        return league_table

    def wubai_get_fight_history(self,odds_content):
        fight_history = []
        for idx, tr in enumerate(odds_content[0].select('.history')[0].select('.M_content')[0].find_all('tr')):
            if idx > 1:
                tds = tr.find_all('td')
                dict1 = {}
                dict1['league'] = tds[0].a.text
                dict1['date'] = tds[1].contents[0]
                dict1['match'] = tds[2].text
                dict1['half'] = tds[3].text
                dict1['result'] = tds[4].span.contents[0]
                dict1['e_odd'] = tds[5].text
                dict1['a_odd'] = tds[6].text
                if tds[7].span == None:
                    dict1['odd_result'] = tds[7].contents[0]
                else:
                    dict1['odd_result'] = tds[7].span.text
                if tds[8].span == None:
                    dict1['daxiao'] = tds[8].contents[0]
                else:
                    dict1['daxiao'] = tds[8].span.text
                fight_history.append(dict1)
        return fight_history

    def wubai_history_fight_summary(self,odds_content):
        return odds_content[0].select('.history')[0].select('.his_info')[0].text

    def wubai_get_recent_match(self,odds_content,team):
        recent = []
        for idx, tr in enumerate(odds_content[0].select('.record')[0].select(team)[0].select('.M_content')[0].find_all('tr')):
            if idx != 0 and idx < 12:
                tds = tr.find_all('td')
                dict1 = {}
                dict1['league'] = tds[0].text
                dict1['date'] = tds[1].contents[0]
                dict1['match'] = tds[2].text
                dict1['odd'] = tds[3].text
                dict1['half'] = tds[4].text
                dict1['result'] = tds[5].text
                if tds[6].span == None:
                    dict1['odd_result'] = tds[6].contents[0]
                else:
                    dict1['odd_result'] = tds[6].span.text
                if tds[7].span == None:
                    dict1['daxiao'] = tds[7].contents[0]
                else:
                    dict1['daxiao'] = tds[7].span.text
                recent.append(dict1)
        return recent

    def wubai_recent_match_summary(self,odds_content,team):
        return odds_content[0].select('.record')[0].select(team)[0].select('.M_content')[0].select('.bottom_info')[0].p.text

    def wubai_get_recent_match_same(self,odds_content,team):
        recent_the_same_land = []
        for idx, tr in enumerate(odds_content[0].select('.record')[0].select(team)[0].select('.M_content')[0].find_all('tr')):
            if idx != 0 and idx < 12:
                tds = tr.find_all('td')
                dict1 = {}
                dict1['league'] = tds[0].text
                dict1['date'] = tds[1].contents[0]
                dict1['match'] = tds[2].text
                dict1['odd'] = tds[3].text
                dict1['half'] = tds[4].text
                dict1['result'] = tds[5].text
                if tds[6].span == None:
                    dict1['odd_result'] = tds[6].contents[0]
                else:
                    dict1['odd_result'] = tds[6].span.text
                if tds[7].span == None:
                    dict1['daxiao'] = tds[7].contents[0]
                else:
                    dict1['daxiao'] = tds[7].span.text
                recent_the_same_land.append(dict1)
        return recent_the_same_land

    def wubai_get_recent_match_same_summary(self,odds_content,team):
        return odds_content[0].select('.record')[0].select('#zhanji_11')[0].select('.M_content')[0].select('.bottom_info')[0].p.text


    def wubai_future_match(self,odds_content,team):
        future_match = []
        for idx, tr in enumerate(odds_content[0].select('.integral')[0].select('.M_content')[0].select(team)[0].find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                dict1 = {}
                dict1['league'] = tds[0].text
                dict1['date'] = tds[1].contents[0]
                dict1['match'] = tds[2].text
                dict1['period'] = tds[3].text
                future_match.append(dict1)
        return future_match



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
    odds_content = base_data.wubai_get_base_data(con)
    team = base_data.get_host_and_away_team(odds_content)
    host_team_league_table = base_data.wubai_get_league_table(odds_content,'.team_a')
    away_team_league_table = base_data.wubai_get_league_table(odds_content,'.team_b')
    fight_history = base_data.wubai_get_fight_history(odds_content)
    fight_history_summary = base_data.wubai_history_fight_summary(odds_content)
    host_recent_match = base_data.wubai_get_recent_match(odds_content,'#team_zhanji_1')
    away_recent_match = base_data.wubai_get_recent_match(odds_content,'#team_zhanji_0')
    host_recent_match_summary = base_data.wubai_recent_match_summary(odds_content,'#team_zhanji_1')
    away_recent_match_summary = base_data.wubai_recent_match_summary(odds_content,'#team_zhanji_0')
    host_recent_match_same = base_data.wubai_get_recent_match_same(odds_content,'#zhanji_11')
    away_recent_match_same = base_data.wubai_get_recent_match_same(odds_content,'#zhanji_20')
    host_recent_match_same_summary = base_data.wubai_get_recent_match_same_summary(odds_content,'#zhanji_11')
    away_recent_match_same_summary = base_data.wubai_get_recent_match_same_summary(odds_content,'#zhanji_20')
    host_future_match = base_data.wubai_future_match(odds_content,'.team_a')
    away_future_match = base_data.wubai_future_match(odds_content,'.team_b')
    t = get_template('match/analyse.html')
    html = t.render(Context({'team': team, 
        'host_team_league_table': host_team_league_table,
        'away_team_league_table': away_team_league_table,
        'fight_history': fight_history,
        'fight_history_summary': fight_history_summary,
        'host_recent_match': host_recent_match,
        'away_recent_match': away_recent_match,
        'host_recent_match_summary': host_recent_match_summary,
        'away_recent_match_summary': away_recent_match_summary,
        'host_recent_match_same': host_recent_match_same,
        'away_recent_match_same': away_recent_match_same,
        'host_recent_match_same_summary': host_recent_match_same_summary,
        'away_recent_match_same_summary': away_recent_match_same_summary,
        'host_future_match': host_future_match,
        'away_future_match': away_future_match
    }))
    return HttpResponse(html)





