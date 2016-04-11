#!/usr/bin/python
# -*- coding: utf-8 -*-  

# Get id No. and name !!!
# By Jack
# 2016年 04月 11日 星期一 21:14:36 CST

import urllib, urllib2, re
url = 'http://www.shenfenzhenghaodaquan.org'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'Michael Foord',
        'location' : 'Northampton',
        'language' : 'Python' }
headers = { 'User-Agent' : user_agent }
data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
html = response.read()
html = html.decode('gb18030').encode('utf-8')
par = re.compile(r'(?<=<br>).*? \d{17}.(?=<br>)', re.X)
match_group = par.search(html)
# lets go into each id
while match_group:
    print match_group.group()
    end = match_group.end()
    html = html[end:]
    match_group = par.search(html)
    
