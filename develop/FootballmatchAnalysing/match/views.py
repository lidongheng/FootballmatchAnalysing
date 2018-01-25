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
        self.yazhi_level = {
        '受四球': '-4.00',
        '受三球半/四球': '-3.75',
        '受三球半': '-3.50',
        '受三球/三球半': '-3.25',
        '受三球': '-3.00',
        '受两球半/三球': '-2.75',
        '受两球半': '-2.50',
        '受两球/两球半': '-2.25',
        '受两球': '-2.00',
        '受球半/两球': '-1.75',
        '受球半': '-1.50',
        '受一球/球半': '-1.25',
        '受一球': '-1.00',
        '受半球/一球': '-0.75',
        '受半球': '-0.50',
        '受平手/半球': '-0.25',
        '平手': '0.00',
        '四球': '4.00',
        '三球半/四球': '3.75',
        '三球半': '3.50',
        '三球/三球半': '3.25',
        '三球': '3.00',
        '两球半/三球': '2.75',
        '两球半': '2.50',
        '两球/两球半': '2.25',
        '两球': '2.00',
        '球半/两球': '1.75',
        '球半': '1.50',
        '一球/球半': '1.25',
        '一球': '1.00',
        '半球/一球': '0.75',
        '半球': '0.50',
        '平手/半球': '0.25',
        }
        self.no1=['曼城']
        self.no2=['曼联','切尔西','利物浦','热刺','阿森纳']
        self.no3=['莱切城','埃弗顿','沃特福']
        self.no4=['西汉姆','水晶宫','斯托克','南安普','西布罗','伯恩利']
        self.no5=['纽卡','布莱顿','哈德斯','伯恩茅','斯旺西']

    def wubai_connect(self):
        reqhd = urllib.request.Request(self.url, headers = self.header)
        req = urllib.request.urlopen(reqhd)
        if req.info().get('Content-Encoding') == 'gzip':
            doc = req.read()
            con = gzip.decompress(doc).decode('gbk')
        else:
            con = req.read().decode('gbk')
        return con

    def t(self,strr):
        list5 = strr.split('.')
        if len(list5) == 1:
            strr = list5[0] + '.00'
        else:
            if len(list5[1]) == 1:
                strr = list5[0] + '.' + list5[1] + '0'
            else:
                strr = list5[0]+'.'+list5[1]
        return strr

    def wubai_get_ouzhi(self,fid):
        params = {}
        params['_'] = str(time.time()*1000).split('.')[0]
        params['fid'] = fid
        params['r'] = '1'
        params['type'] = 'europe'
        company = {'1':'竞彩', '293':'威廉希尔', '2':'立博', '3':'Bet365', '6': '韦德', '4':'Interwetten', '5': '澳彩', '122':'香港马会'}
        company_list = [1,293,2,3,6,4,5,122]
        wubai_ouzhi = {}
        for item in company_list:
            url = self.url+'?'+'_='+params['_']+"&fid="+params['fid']+"&cid="+str(item)+"&r="+params['r']+"&type="+params['type']
            print(url)
            reqhd = urllib.request.Request(url, headers = self.header)
            req = urllib.request.urlopen(reqhd)
            if req.info().get('Content-Encoding') == 'gzip':
                doc = req.read()
                con = gzip.decompress(doc).decode('gbk')
            else:
                con = req.read().decode('gbk')
            array_str = con.strip()[1:-1]
            print(array_str)
            list1 = re.findall(r'\[.*?\]', array_str, re.S)
            print(list1)
            list2 = []
            if len(list1) == 1:
                dict1 = {}
                list1 = list1[0][1:-1].split(',')
                dict1['order'] = str(item)
                dict1['ori_win_odd'] = self.t(list1[0])
                dict1['ori_tie_odd'] = self.t(list1[1])
                dict1['ori_def_odd'] = self.t(list1[2])
                dict1['ori_peifu'] = list1[3]
                dict1['ori_time'] = list1[4][1:-1]
                dict1['now_win_odd'] = self.t(list1[0])
                dict1['now_tie_odd'] = self.t(list1[1])
                dict1['now_def_odd'] = self.t(list1[2])
                dict1['now_peifu'] = list1[3]
                dict1['now_time'] = list1[4][1:-1]
                dict1['now_win_cond'] = '0'
                dict1['now_tie_cond'] = '0'
                dict1['now_def_cond'] = '0'
                wubai_ouzhi[company[str(item)]] = dict1
            else:
                list2.append(list1[-1][1:-1].split(','))
                list2.append(list1[0][1:-1].split(','))
                dict1 = {}
                dict1['order'] = str(item)
                dict1['ori_win_odd'] = self.t(list2[0][0])
                dict1['ori_tie_odd'] = self.t(list2[0][1])
                dict1['ori_def_odd'] = self.t(list2[0][2])
                dict1['ori_peifu'] = list2[0][3]
                dict1['ori_time'] = list2[0][4][1:-1]
                dict1['now_win_odd'] = self.t(list2[1][0])
                dict1['now_tie_odd'] = self.t(list2[1][1])
                dict1['now_def_odd'] = self.t(list2[1][2])
                dict1['now_peifu'] = list2[1][3]
                dict1['now_time'] = list2[1][4][1:-1]
                dict1['now_win_cond'] = list2[1][5]
                dict1['now_tie_cond'] = list2[1][6]
                dict1['now_def_cond'] = list2[1][7]
                wubai_ouzhi[company[str(item)]] = dict1
        return wubai_ouzhi

    def wubai_get_yazhi(self):
        con = self.wubai_connect()
        soup = BeautifulSoup(con, 'html5lib')
        yazhi = soup.select('.odds_yazhi')
        trs = yazhi[0].find_all('table')[3].tbody.find_all('tr')
        wubai_yazhi = []
        for idx, tr in enumerate(trs):
            if idx%3 == 0:
                tds = tr.find_all('td')
                dict1 = {}
                dict1['order'] = tds[0].text.strip()
                dict1['company'] = tds[1].span.text
                dict1['now_up_odd'] = tds[3].text
                now_ya = tds[4].text.split(' ')[0]
                dict1['now_ya_odd'] = now_ya
                dict1['now_ya_odd_shuzi'] = self.yazhi_level[now_ya]
                dict1['now_down_odd'] = tds[5].text
                dict1['now_time'] = tds[7].text
                dict1['ori_up_odd'] = tds[9].text
                dict1['ori_ya_odd'] = tds[10].text
                dict1['ori_ya_odd_shuzi'] = self.yazhi_level[tds[10].text]
                dict1['ori_down_odd'] = tds[11].text
                dict1['ori_time'] = tds[12].text
                wubai_yazhi.append(dict1)
        return wubai_yazhi

    def wubai_get_guangshi(hometeam,visitingteam):
        if hometeam in self.no1:
            if visitingteam !='阿森纳':
                if visitingteam in self.no2:
                    t='1'
                elif visitingteam in self.no3:
                    t='2'                
                elif visitingteam in self.no4:
                    t='2.5'                
                elif visitingteam in self.no5:
                   t='2.75'
                else:
                    return False
                return t
            else:
                t='1.25'
                return t
        if hometeam in self.no2:
            if hometeam =='阿森纳' and visitingteam in self.no1:
                t='-0.5'
                return t
            elif hometeam =='阿森纳' and visitingteam in self.no2:
                t='0'
                return t
            if visitingteam == '阿森纳':
                t='0.5'
                return t
            if visitingteam in self.no1:
                t='-0.25'     
            elif visitingteam in self.no2:
                t='0.25'
            elif visitingteam in self.no3:
                t='1 1.25'
            elif visitingteam in self.no4:
                t='1.5'
            elif visitingteam in self.no5:
                t='1.75 2'
            else:
                return False
            return t

        if hometeam in self.no3:
            if visitingteam in self.no1:
                t='-1.5 -1.25'
            elif visitingteam in self.no2:
                t='-0.75'
            elif visitingteam in self.no3:
                t='0.25'
            elif visitingteam in self.no4:
                t='0.5'
            elif visitingteam in self.no5:
                t='0.75'
            return t

        if hometeam in no4:
            if visitingteam in self.no1:
                t='-1.5'
            elif visitingteam in self.no2:
                t='-1'
            elif visitingteam in self.no3:
                t='0'
            elif visitingteam in self.no4:
                t='0.25'
            elif visitingteam in self.no5:
                t='0.5'
            return t

        if hometeam in self.no5:
            if visitingteam == '阿森纳':
                t='-1'
                return t
            if visitingteam == '伯恩利':
                t='0.25'
                return t
            if visitingteam in self.no1:
                t='-1.75'
            elif visitingteam in self.no2:
                t='-1.25'
            elif visitingteam in self.no3:
                t='-0.25'
            elif visitingteam in self.no4:
                t='0'
            elif visitingteam in self.no5:
                t='0.25'
            else:
                return False
            return t

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
                dict1['time'] = tds[1].contents[0]
                temp = tds[2].text.strip().split('VS')
                dict1['host_team'] = temp[0].strip()
                dict1['away_team'] = temp[1].strip()
                dict1['day'] = tds[3].text
                dict1['hours'] = '-'
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
    '日职': '109',
    '澳超': '283',
    '欧冠': '10',
    '欧罗巴': '18',
    '亚冠杯': '251',
    '日职乙': '110',
    '英足总杯': '93',
    '英联杯': '95',
    '西班牙杯': '138',
    '意杯': '135',
    '日联杯': '223',
    '天皇杯': '577',
    '世界杯': '72',
    '友谊赛': '430',}
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
        big_month = [1,3,5,7,8,10,12]
        small_month = [2,4,6,9,11]
        by,bmon,bd,bh,bm,bs = self.__wangyi_date_handle(match_time)
        t1 = datetime.datetime(by,bmon,bd,bh,bm,bs)
        for idx, tr in enumerate(teams[0].find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                host_future_time = '20'+tds[1].text+':00'
                cy,cmon,cd,ch,cm,cs = self.__wangyi_date_handle(host_future_time)
                daya = int(cd)-int(bd)
                if daya < 0:
                    if bmon in big_month:
                        daya = 31 - bd + cd
                    else:
                        if bmon == 2:
                            if by%4 == 0:
                                daya = 29 - bd + cd
                            else:
                                daya = 28 - bd + cd
                        else:
                            daya = 30 - bd + cd
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
                if dayb < 0:
                    if bmon in big_month:
                        dayb = 31 - bd + dd
                    else:
                        if bmon == 2:
                            if by%4 == 0:
                                dayb = 29 - bd + dd
                            else:
                                dayb = 28 - bd + dd
                        else:
                            dayb = 30 - bd + dd
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

def all_get_future_match(wubai_host_future_match,wubai_away_future_match,wangyi_host_future_match,wangyi_away_future_match):
    '''
    先删除本场比赛，再合并两个网站的数据
    '''
    if len(wangyi_host_future_match) < 5 and len(wangyi_away_future_match) < 5:
        return wangyi_host_future_match,wangyi_away_future_match
    host_future_match = []
    away_future_match = []
    '''
    先确定主队和客队
    '''
    if len(wangyi_host_future_match) >= 3:
        a = wangyi_host_future_match[0]['host_team']
        b = wangyi_host_future_match[0]['away_team']
        c = wangyi_host_future_match[1]['host_team']
        d = wangyi_host_future_match[1]['away_team']
        e = wangyi_host_future_match[2]['host_team']
        f = wangyi_host_future_match[2]['away_team']
        if (a == c) or (a == d):
            if (a == e) or (a == f):
                host_team = a
        else:
            if (b == c) or (b == d):
                host_team = b
    if len(wangyi_away_future_match) >= 3:
        a = wangyi_away_future_match[0]['host_team']
        b = wangyi_away_future_match[0]['away_team']
        c = wangyi_away_future_match[1]['host_team']
        d = wangyi_away_future_match[1]['away_team']
        e = wangyi_away_future_match[2]['host_team']
        f = wangyi_away_future_match[2]['away_team']
        if (a == c) or (a == d):
            if (a == e) or (a == f):
                away_team = a
        else:
            if (b == c) or (b == d):
                away_team = b
    if wangyi_host_future_match[0]['host_team'] == host_team and wangyi_host_future_match[0]['away_team'] == away_team:
        wangyi_host_future_match = wangyi_host_future_match[1:]
    if wangyi_away_future_match[0]['host_team'] == host_team and wangyi_away_future_match[0]['away_team'] == away_team:
        wangyi_away_future_match = wangyi_away_future_match[1:]
    for index in range(0,len(wubai_host_future_match)):
        if len(wangyi_host_future_match) > index:
            host_future_match.append(wangyi_host_future_match[index])
        else:
            host_future_match.append(wubai_host_future_match[index])
        if len(wangyi_away_future_match) > index:
            away_future_match.append(wangyi_away_future_match[index])
        else:
            away_future_match.append(wubai_away_future_match[index])
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
    wubai_host_future_match = base_data.wubai_future_match(odds_content,'.team_a')
    wubai_away_future_match = base_data.wubai_future_match(odds_content,'.team_b')
    match_round = base_data.wubai_get_match_round(con)
    host_league_name = base_data.wubai_get_host_team_league_name(team[0])
    add_data = Adddata()
    url = add_data.wangyi_get_page_url(host_league_name,match_round)
    wangyi_host_future_match,wangyi_away_future_match = add_data.wangyi_get_future_match(url)
    host_future_match,away_future_match = all_get_future_match(wubai_host_future_match,wubai_away_future_match,wangyi_host_future_match,wangyi_away_future_match)
    wubai_odds_url = 'http://odds.500.com/fenxi1/json/ouzhi.php'
    odds_data = Basedata(wubai_odds_url,wubai_hds)
    wubai_ouzhi = odds_data.wubai_get_ouzhi(fid)
    yazhi_url = 'http://odds.500.com/fenxi/yazhi-'+fid+'.shtml?ctype=2'
    yazhi_data = Basedata(yazhi_url,wubai_hds)
    wubai_yazhi = yazhi_data.wubai_get_yazhi()
    wubai_guangshi = yazhi_data.wubai_get_guangshi(team[0],team[1])
    if not guangshi:
        wubai_guangshi = '无'
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
        'wubai_ouzhi': wubai_ouzhi,
        'wubai_yazhi': wubai_yazhi,
        'wubai_guangshi': wubai_guangshi,
    }))
    return HttpResponse(html)





