#coding:utf-8
str1 = '0.85'
print str1
print str1[1:2]
print str1[2:3]
a = float(str1) * 100
if a > 85:
    print 1
elif a<85:
    print 2
else:
    print 3
standard_odd_str = [['2.62','3.30','2.65'],['2.50','3.50','2.62'],['2.45','3.30','2.80'],['2.40','3.30','2.87'],['2.38','3.30','2.90']]
for item in standard_odd_str:
    print item[0]