no1=['曼城']
no2=['曼联','切尔西','利物浦','热刺','阿森纳']
no3=['莱斯特城','埃弗顿','沃特福德']
no4=['西汉姆联','水晶宫','斯托克城','南安普顿','西布朗维奇']
no5=['伯恩利','纽卡斯尔','布莱顿','哈德斯菲尔德','伯恩茅斯','斯旺西']



rare_dict={'受四球': '-4',
        '受三球半/四球': '-3.75',
        '受三球半': '-3.5',
        '受三球/三球半': '-3.25',
        '受三球': '-3',
        '受两球半/三球': '-2.75',
        '受两球半': '-2.5',
        '受两球/两球半': '-2.25',
        '受两球': '-2',
        '受球半/两球': '-1.75',
        '受球半': '-1.5',
        '受一球/球半': '-1.25',
        '受一球': '-1',
        '受半球/一球': '-0.75',
        '受半球': '-0.5',
        '受平手/半球': '-0.25',
        '平手': '0',
        '四球': '4',
        '三球半/四球': '3.75',
        '三球半': '3.5',
        '三球/三球半': '3.25',
        '三球': '3',
        '两球半/三球': '2.75',
        '两球半': '2.5',
        '两球/两球半': '2.25',
        '两球': '2',
        '球半/两球': '1.75',
        '球半': '1.5',
        '一球/球半': '1.25',
        '一球': '1',
        '半球/一球': '0.75',
        '半球': '0.5',
        '平手/半球': '0.25'}

def print_rare(t):
    print(hometeam+' '+list(rare_dict.keys())[list(rare_dict.values()).index(t)]+' '+visitingteam)

def compare(hometeam,visitingteam):
    
    if hometeam in no1:
        if visitingteam !='阿森纳':
            if visitingteam in no2:
                t='1'
            elif visitingteam in no3:
                t='2'                
            elif visitingteam in no4:
                t='2.5'                
            elif visitingteam in no5:
                t='2.75'
            else:
                print('没有此比较')
            print_rare(t)
        else:
            t='2'
            print_rare(t)
    if hometeam in no2:
        if hometeam !='阿森纳':
            if visitingteam in no1:
                t='-0.25'     
            elif visitingteam in no2:
                t='0.25'
            elif visitingteam in no3:
                print(hometeam+' ' + '一球或一球/球半'+' '+visitingteam)
            elif visitingteam in no4:
                t='1.5'
            elif visitingteam in no5:
                t='2'
            else:
                print('没有此比较')
        else:
            if visitingteam in no1:
                t='-0.25'
            if visitingteam in no2:
                t='0.25'
        print_rare(t)
            
    if hometeam in no3:
        if visitingteam in no1:
            print(hometeam+' ' + '受球半 或受一球/球半 '+' '+visitingteam)
        elif visitingteam in no2:
            t='-0.75'
        elif visitingteam in no3:
            t='0.25'
        elif visitingteam in no4:
            t='0.5'
        elif visitingteam in no5:
            t='0.75'
        print_rare(t)
        
    if hometeam in no4:
        if visitingteam in no1:
            t='-1.5'
        elif visitingteam in no2:
            t='-1'
        elif visitingteam in no3:
            t='0'
        elif visitingteam in no4:
            t='0.25'
        elif visitingteam in no5:
            t='0.5'
        print_rare(t)

    if hometeam in no5:
        if visitingteam in no1:
            t='-1.75'
        elif visitingteam in no2:
            t='-1.25'
        elif visitingteam in no3:
            t='-0.25'
        elif visitingteam in no4:
            t='0'
        elif visitingteam in no5:
            t='0.25'
            
hometeam=input('请输入主队:')
visitingteam = input('请输入客队:')
compare(hometeam,visitingteam)
        
    
