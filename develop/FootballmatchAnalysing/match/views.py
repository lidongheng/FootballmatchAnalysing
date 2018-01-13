#coding:utf-8
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
import urllib
import re
from bs4 import BeautifulSoup
import gzip
import operator
import time
import datetime

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
            fid = soup.tr.attrs['fid']
            tr = soup.find_all('tr')[0]
            tds = tr.find_all('td')
            list1.append({
                'fid': fid,
                'number': tds[0].a.contents[0],
                'league': tds[1].text,
                'time': tds[2].span.text,
                'host_team': tds[3].a.contents[0],
                'away_team': tds[5].a.contents[0],
            })
        return list1
    def wubai_get_match_round(self, con):
        soup = BeautifulSoup(con, 'html5lib')
        tds = soup.select('.odds_header')[0].table.tbody.tr.find_all('td')
        match_str = tds[2].div.a.contents[0].rstrip()
        match_round = int(re.findall(r'[0-9]+',match_str,re.S)[-1:][0])
        return match_round

    def wubai_get_base_data(self, con):
        soup = BeautifulSoup(con, 'html5lib')
        odds_content = soup.select('.odds_content')
        return odds_content

    def wubai_get_host_and_away_team(self, odds_content):
        team = []
        team.append(odds_content[0].select('.M_sub_title')[0].select('.team_name')[0].text)
        team.append(odds_content[0].select('.M_sub_title')[0].select('.team_name')[1].text)
        return team

    def wubai_get_host_team_league_name(self,str):
        team_tuple = re.findall(r'(^.*?)\[(.*?)[0-9].*\]', str)
        team = list(team_tuple[0])
        return team

    def wubai_get_league_table(self,odds_content,team):
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
        return odds_content[0].select('.record')[0].select(team)[0].select('.M_content')[0].select('.bottom_info')[0].p.text


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

class Adddata(object):

    def __init__(self):
        self.wangyi_league={
    '西甲': '7',
    '英超': '8',
    '意甲': '13',
    '德甲': '9',
    '法甲': '16',
    '葡超': '63',
    '俄超': '121',
    '日职': '109',}
        self.wubai_to_wangyi={
    '马竞技': '马竞',
    '塞维利': '塞维利亚',
    '拉科鲁': '拉科',
    '社会': '皇家社会',
    '毕尔巴': '毕尔巴鄂',
    '皇马': '皇马',
    '巴萨': '巴萨',
    '莱加内': '莱加内斯',
    '比利亚': '比利亚雷',
    '巴伦西': '巴伦西亚',
    '西牙人': '西班牙人',
    '拉斯帕': '拉帕马斯',
    '阿拉维': '阿拉维斯',
    '纽卡': '纽卡斯尔',
    '莱切城': '莱切斯特',
    '斯托克': '斯托克城',
    '沃特福': '沃特福德',
    '热刺': '热刺',
    '西布罗': '西布罗姆',
    '曼联': '曼联',
    '伯恩茅': '伯恩茅斯',
    '南安普': '南安普敦',
    '曼城': '曼城',
    '西汉姆': '西汉姆联',
    '罗马': '罗马',
    '士柏': '费拉拉',
    '那不勒': '那不勒斯',
    '尤文': '尤文图斯',
    '都灵': '都灵',
    '亚特兰': '亚特兰大',
    '贝内文': '贝内文托',
    '博洛尼': '博洛尼亚',
    '卡利亚': '卡利亚里',
    '佛罗伦': '佛罗伦萨',
    '国米': '国际米兰',
    '切沃': '切沃',
    '桑普多': '桑普',
    '克罗托': '克罗托内',
    '乌迪内': '乌迪内斯',
    '汉堡': '汉堡',
    '奥格斯': '奥格斯堡',
    '勒沃': '勒沃库森',
    '多特': '多特蒙德',
    '拜仁': '拜仁',
    '汉诺威': '汉诺威9',
    '霍芬': '霍芬海姆',
    '莱比锡': '莱红牛',
    '斯图加': '斯图加特',
    '沙尔克': '沙尔克0',
    '科隆': '科隆',
    '赫塔': '柏林赫塔',
    '法兰克': '法兰克福',
    '沃尔夫': '沃夫斯堡',
    '门兴': '门兴',}
    def __wangyi_connect(self,url,header):
        reqhd = urllib.request.Request(url, headers = header)
        req = urllib.request.urlopen(reqhd)
        if req.info().get('Content-Encoding') == 'gzip':
            doc = req.read()
            con = gzip.decompress(doc).decode('utf-8')
        else:
            con = req.read().decode('utf-8')
        return con

    def __wangyi_date_handle(self,timestr):
        year = int(timestr[0:4])
        month = int(timestr[5:7])
        day = int(timestr[8:10])
        hour = int(timestr[11:13])
        minute = int(timestr[14:16])
        second = 0
        return year,month,day,hour,minute,second

    def wangyi_get_page_url(self,team_league,match_round):
        league = self.wangyi_league[team_league[1]]
        url = 'http://saishi.caipiao.163.com/'+league+'.html?weekId='+str(match_round)+'&groupId=&roundId=42011&indexType=0&guestTeamId='
        header = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
            "Accept-Language": "zh-CN,zh;q=0.8", 
            "Accept-encoding": "gzip, deflate",
            "Cache-Control": "no-cache", 
            "Connection": "keep-alive", 
            "Host": "saishi.caipiao.163.com", 
            "Referer": url,
            "Upgrade-Insecure-Requests": "1", 
            "Pragma": "no-cache",
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        con = self.__wangyi_connect(url,header)
        soup = BeautifulSoup(con, 'html5lib')
        for idx, a in enumerate(soup.select('.analyseBody')[0].find_all('a')):
            try:
                name = self.wubai_to_wangyi[team_league[0]]
            except KeyError:
                name = team_league[0]
            if operator.eq(a.span.contents[0], name):
                url = a.attrs['href']
                break
        return url
    def wangyi_get_future_match(self,url):
        header = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
            "Accept-Language": "zh-CN,zh;q=0.8", 
            "Accept-encoding": "gzip, deflate",
            "Cache-Control": "no-cache", 
            "Connection": "keep-alive", 
            "Host": "bisai.caipiao.163.com", 
            "Upgrade-Insecure-Requests": "1", 
            "Pragma": "no-cache",
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        con = self.__wangyi_connect(url,header)
        soup = BeautifulSoup(con, 'html5lib')
        match_time = soup.select('.date')[0].text
        teams = soup.find_all('section')[8].find_all('table')
        host_future_match = []
        away_future_match = []
        by,bmon,bd,bh,bm,bs = self.__wangyi_date_handle(match_time)
        t1 = datetime.datetime(by,bmon,bd,bh,bm,bs)
        for idx, tr in enumerate(teams[0].find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                host_future_time = '20'+tds[1].text+':00'
                cy,cmon,cd,ch,cm,cs = self.__wangyi_date_handle(host_future_time)
                daya = int(cd)-int(bd)
                t2 = datetime.datetime(cy,cmon,cd,ch,cm,cs)
                hoursa = int((t2-t1).total_seconds()/3600)
                host_future_match.append({
                    'league':tds[0].text,
                    'time':host_future_time,
                    'host_team':tds[2].text.strip(),
                    'away_team':tds[3].a.contents[0],
                    'day': daya,
                    'hours': hoursa,
                })
        for idx, tr in enumerate(teams[1].find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                away_future_time = '20'+tds[1].text+':00'
                dy,dmon,dd,dh,dm,ds = self.__wangyi_date_handle(away_future_time)
                dayb = int(dd)-int(bd)
                t3 = datetime.datetime(dy,dmon,dd,dh,dm,ds)
                hoursb = int((t3-t1).total_seconds()/3600)
                away_future_match.append({
                    'league':tds[0].text,
                    'time': away_future_time,
                    'host_team':tds[2].text.strip(),
                    'away_team':tds[3].a.contents[0],
                    'day': dayb,
                    'hours': hoursb,
                })
        return host_future_match,away_future_match



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
    fid = request.GET['fid']
    if fid == None:
        return HttpResponseRedirect('/index/')
    wubai_url = 'http://odds.500.com/fenxi/shuju-'+fid+'.shtml'
    wubai_hds = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
    "Accept-Language": "zh-CN,zh;q=0.8", 
    "Accept-encoding": "gzip",
    "Cache-Control": "no-cache", 
    "Connection": "keep-alive", 
    "Host": "odds.500.com", 
    "Upgrade-Insecure-Requests": "1", 
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
    base_data = Basedata(wubai_url,wubai_hds)
    con = base_data.wubai_connect()
    odds_content = base_data.wubai_get_base_data(con)
    team = base_data.wubai_get_host_and_away_team(odds_content)
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
    #host_future_match = base_data.wubai_future_match(odds_content,'.team_a')
    #away_future_match = base_data.wubai_future_match(odds_content,'.team_b')
    match_round = base_data.wubai_get_match_round(con)
    host_league_name = base_data.wubai_get_host_team_league_name(team[0])
    add_data = Adddata()
    url = add_data.wangyi_get_page_url(host_league_name,match_round)
    host_future_match,away_future_match = add_data.wangyi_get_future_match(url)
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
        'away_future_match': away_future_match,
    }))
    return HttpResponse(html)





