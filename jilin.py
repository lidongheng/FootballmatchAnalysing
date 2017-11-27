# -*- coding: utf-8 -*-
from urllib import request
url = "http://gxzn168.com/"
req = request.urlopen(url)
print (req.code)