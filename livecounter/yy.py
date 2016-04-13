#!/usr/bin/python
# -*- coding: utf-8 -*-  

# F**k off yy.com !!!
# By Jack
# 2016年 04月 13日 星期三 16:30:23 CST

import urllib2 as ul, urllib, re, json, time

sleep_time = 0.5

def find_par(url):
    par_pbiz = re.compile(r'(?<=/)\w+$', re.X)
    par_serv = re.compile(r'(?<=liveServ\W=\W")\d+(?=")', re.X)
    par_idid = re.compile(r'(?<=liveId\W=\W")\d+(?=")', re.X)
    html = ul.urlopen( ul.Request(url) ).read()
    return [ par_pbiz.search(url).group(),
             par_serv.search(html).group(),
             par_idid.search(html).group() ] 

def fk(cate, url):
    timer = time.ctime()
    [ pbiz, serv, id ] = find_par(url)
    act_url = 'http://www.yy.com/ent/index/pageLive.action'
    page = 0
    islast = 0
    sum = 0
    channel = 0
    
    while islast == 0:
        page += 1
        data = {'pbiz': pbiz, 'serv': serv, 'id': id, 'page': page}
        data = urllib.urlencode(data)
        html = ul.urlopen( ul.Request(act_url, data)).read()
        time.sleep(sleep_time)
        js_data = json.loads(html)
        islast = js_data['data']['isLastPage']
        for item in js_data['data']['data']:
            sum += item['users']
            channel += 1
    print ','.join([cate, timer, str(channel), str(sum)])

data_dic = {}
act_url = 'http://www.yy.com/ent/index/pageLive.action'
#print ','.join(['分类','时间','直播数目','在线人数'])

# check index
index = 'http://www.yy.com'
html = ul.urlopen( ul.Request(index) ).read()
start = html.find('yy.com"')
end = html.find('其他')
html = html[start:end+15]
head_par = re.compile(r'(?<=href=")http:.*?(?=")', re.X)
cate_par = re.compile(r'(?<=span>).*?(?=</span)', re.X)

head_match_group = head_par.search(html)
# lets go into each head
while head_match_group:
    end = head_match_group.end()
    html = html[end:]
    cate_match_group = cate_par.search(html)
    head = head_match_group.group()
    cate = cate_match_group.group()
    head_match_group = head_par.search(html)
    data_dic[cate] = head

for i in data_dic:
    if 'ent' in data_dic[i]:
        fk(i, data_dic[i])
