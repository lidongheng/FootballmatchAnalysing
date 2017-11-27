# -*- coding: utf-8 -*-
from urllib import request
import re
url = "https://movie.douban.com/top250"
req = request.urlopen(url)
con = req.read().decode('utf-8')
rs = re.findall(r'<li>(.*?)</li>', con, re.S)
for item in rs[1:27]:
    img = re.findall(r'<img.*?>', item)
    result = img[0].split(' ')
    imgurl = [i.split("=")[1].strip('"') for i in result[1:4]]
    imgreq = request.urlopen(imgurl[2])
    imginfo = imgreq.read()
    imgf = open('/home/ldh/Projects/scrapy_1.0/'+imgurl[1]+'.jpg', 'wb')
    imgf.write(imginfo)
    imgf.close()
