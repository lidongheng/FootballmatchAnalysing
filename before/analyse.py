#coding:utf-8
def Asia_odd_water(water):
    water = float(water) * 100
    if water < 78:
        str1 = '超低水'
    elif water >=78 and water<=83:
        str1 = '低水'
    elif water>83 and water<=88:
        str1 = '中低水'
    elif water>88 and water<=93:
    	str1 = '中水'
    elif water >93 and water <=98:
        str1 = '中高水'
    elif water >98 and water <=103:
        str1 = '高水'
    else:
        str1 = '超高水'
    return str1

def williamhill_nightyfour_odd():
    if aisa_odd == '0':
        standard_odd = [[2.62,3.30,2.65],[2.50,3.50,2.62],[2.45,3.30,2.80],[2.40,3.30,2.87],[2.38,3.30,2.90]]
        standard_odd_str = [['2.62','3.30','2.65'],['2.50','3.50','2.62'],['2.45','3.30','2.80'],['2.40','3.30','2.87'],['2.38','3.30','2.90']]
        flag1 = False
        flag2 = False
        if float(win_odd) >= 2.80:
        	flag2 = True
            temp = win_odd
            win_odd = def_odd
            def_odd = temp
        for item in standard_odd_str:
        	if win_odd == item[0]:
        	    nightyfour_win = item[0]
        	    nightyfour_tie = item[1]
        	    nightyfour_def = item[2]
        	    flag = True
        	    break
        if not flag1:
            '''
            判断赔率接近哪个区间
            '''
            if win_odd[2:3] == '3':
                nightyfour_win = standard_odd_str[4][0]
                nightyfour_tie = standard_odd_str[4][1]
        	    nightyfour_def = standard_odd_str[4][2]
        	elif win_odd[2:3] == '4':
        		nightyfour_win = standard_odd_str[2][0]
                nightyfour_tie = standard_odd_str[2][1]
        	    nightyfour_def = standard_odd_str[2][2]
        	elif win_odd[2:3] == '5':
        		nightyfour_win = standard_odd_str[1][0]
                nightyfour_tie = standard_odd_str[1][1]
        	    nightyfour_def = standard_odd_str[1][2]
        	elif win_odd[2:3] == '6':
        		nightyfour_win = standard_odd_str[0][0]
                nightyfour_tie = standard_odd_str[0][1]
        	    nightyfour_def = standard_odd_str[0][2]
        	else:
        		return False
        if flag2:
            flag2 = False
            temp = nightyfour_win
            nightyfour_win = nightyfour_def
            nightyfour_def = temp
        return [nightyfour_win,nightyfour_tie,nightyfour_def]
    else:
        return False


def analyse():
	message = '本场比赛亚盘以'
    if Asia_odd == '0':
    	host_asia_ori_water = float(???)*100
    	away_asia_ori_water = float(???)*100
    	if host_asia_ori_water <= away_asia_ori_water:
            message+='主让平手盘'
            Asia_odd_shang_ori_water = Asia_odd_water(host_asia_ori_water)
            message+=Asia_odd_shang_ori_water
            message+='开盘，受注后上盘水位'
            if host_asia_ori_water<host_asia_now_water:
                message+='上升。'
            else:
                message+='下降。'
        else:
            message+='客让平手盘'
            Aisa_odd_xia_ori_water = Asia_odd_water(away_asia_ori_water)
            message+=Aisa_odd_xia_ori_water
            message+='开盘，受注后上盘水位'
            if away_asia_ori_water<away_asia_now_water:
                message+='上升。'
            else:
                message+='下降。'
        message+='欧赔方面，威廉初赔：'
        message = message + '%s %s %s，' %(???,???,???)
        nighty_four_odd = williamhill_nightyfour_odd()
        '''
        初赔与94赔体系赔率比较
        '''
        message+='与威廉94赔体系相比，(比较赔率的话)'
        message+='目前赔率(即时赔)(然后比较胜平负赔)(再与94赔比较一次)(然后比较胜平负赔)'
        '''
        过往战绩函数
        主队近期状态函数
        客队近期状态函数
        积分榜
        未来赛程
        总共5个函数，然后得出拉力。
        '''
        