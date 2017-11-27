#coding:utf-8
import re
from urllib import request

base_url = 'https://movie.douban.com/top250?start=%d&filter='

class spider_douban250(object):
    def __init__(self, url = None, start = 0, step = 25, total = 250):
        self.durl = url
        self.dstart = start
        self.dstep = step
        self.dtotal = total
        self.dstart += self.dstep

    def start_download(self):
        while self.dstart < self.dtotal:
            durl = self.durl%self.dstart
            self.load_page(durl)

    def load_page(self, url):
        print (url)
        req = request.urlopen(url)
        if req.code != 200:
            return
        con = req.read().decode('utf-8')
        listli = re.findall(r'<li>(.*?)</li>', con, re.S)
        if listli:
            listli=listli[1:]
        else:
            return
        for li in listli:
            imginfo = re.findall(r'<img.*?>', li)
            if imginfo:
                imginfo = imginfo[0]
                print (imginfo)
                result = imginfo.split('alt=')[1]
                result = result.split(' src=')
                imgurl = result[1].split(' ')[0].strip()
                result[1] = imgurl
                info = [item.strip()[1:-1] for item in result]
                #info = [item.split('=').strip()[1:-1] for item in imginfo.split(' ')[1:3]]
                self.load_img(info)

    def load_img(self, info):
        imgreq = request.urlopen(info[1])
        img_c = imgreq.read()
        imgf = open('F:\\test\\'+info[0]+'.jpg', 'wb')
        imgf.write(img_c)
        imgf.close()

spider = spider_douban250(base_url, start=0, step=25, total=25)
spider.start_download()

