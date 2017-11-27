# -*- coding: utf-8 -*-
from urllib import request
import re

base_url = 'https://movie.douban.com/top250?start=%d&filter='

class douban_spider(object):
    def __init__(self, url=None, start=0, step=25, total=25):
        self.durl = url
        self.dstart = start
        self.dstep = step
        self.dtotal = total

    def start_download(self):
        while self.dstart < self.dtotal:
            self.dstart += self.dstep
            durl = self.durl%self.dstart
            self.load_page(durl)

    def load_page(self, url):
        print (url)
        req = request.urlopen(url)
        #if req.code != 200:
        #    return
        con = req.read().decode('utf-8')
        listli = re.findall(r'<li>(.*?)</li>', con, re.S)
        #if listli:
        listli = listli[1:]
        #else:
        #    return
        for li in listli:
            imginfo = re.findall(r'<img.*?>', li)
            if imginfo:
                imginfo = imginfo[0]
                info = []
                result = imginfo.split('alt=')[1]
                result = result.split(' src=')
                info = [item.split(' ')[0].strip('"') for item in result]
                print (info)
                self.load_img(info)
            else:
                return

    def load_img(self, info):
        imgreq = request.urlopen(info[1])
        img_c = imgreq.read()
        imgf = open('/home/ldh/Projects/scrapy_1.0/images/'+info[0]+'.jpg', 'wb')
        imgf.write(img_c)
        imgf.close()

spider = douban_spider(base_url, start=0, step=25, total=250)
spider.start_download()
