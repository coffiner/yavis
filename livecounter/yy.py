#!/usr/bin/python
# -*- coding: utf-8 -*-  

# F**k off yy.com !!!
# By Jack
# 2016年 04月 13日 星期三 16:30:23 CST

import urllib2 as ul, urllib, re, json, time

sleep_time = 0.2
ent_url = 'http://www.yy.com/ent/index/pageLive.action'
t_url = 'http://www.yy.com/more/page.action?biz=BBB&subBiz=idx&page=PPP&moduleId=MMM'

def find_t(url):
    par_biz = re.compile(r'(?<=/)\w+$', re.X)
    par_mid = re.compile(r'(?<=/idx/)\d+(?=")', re.X)
    html = ul.urlopen( ul.Request(url) ).read()
    return [ par_biz.search(url).group(),
             par_mid.search(html).group() ]

def fk_t(cate, url):
    timer = time.ctime()
    [ biz, mid ] = find_t(url)
    uo = t_url
    uo = uo.replace('BBB', biz).replace('MMM', mid)
    page = 0
    sum = 0
    channel = 0
    data = [ 1, 2 ]
    while data:
        page += 1
        u = uo.replace('PPP', str(page))
        html = ul.urlopen( ul.Request(u)).read()
        time.sleep(sleep_time)
        data = json.loads(html)
        tt= data['data']['totalCount']
        data = data['data']['data']
        for item in data:
            sum += item['users']
            channel += 1
    print ','.join([cate, timer, str(channel), str(sum)])

def find_ent(url):
    par_pbiz = re.compile(r'(?<=/)\w+$', re.X)
    par_serv = re.compile(r'(?<=liveServ\W=\W")\d+(?=")', re.X)
    par_idid = re.compile(r'(?<=liveId\W=\W")\d+(?=")', re.X)
    html = ul.urlopen( ul.Request(url) ).read()
    return [ par_pbiz.search(url).group(),
             par_serv.search(html).group(),
             par_idid.search(html).group() ] 

def fk_ent(cate, url):
    timer = time.ctime()
    [ pbiz, serv, id ] = find_ent(url)
    page = 0
    islast = 0
    sum = 0
    channel = 0
    
    while islast == 0:
        page += 1
        data = {'pbiz': pbiz, 'serv': serv, 'id': id, 'page': page}
        data = urllib.urlencode(data)
        html = ul.urlopen( ul.Request(ent_url, data)).read()
        time.sleep(sleep_time)
        js_data = json.loads(html)
        islast = js_data['data']['isLastPage']
        for item in js_data['data']['data']:
            sum += item['users']
            channel += 1
    print ','.join([cate, timer, str(channel), str(sum)])

data_ent = {}
data_t = {}
print ','.join(['栏目','抓取时间','频道数','在线人数'])

# check index
index = 'http://www.yy.com'
html = ul.urlopen( ul.Request(index) ).read()
start = html.find('yy.com"')
end = html.find('其他')
html = html[start:end+15]
head_par = re.compile(r'(?<=href=")\W?http:.*?(?=")', re.X)
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
    if '/ent/' in head:
        data_ent[cate] = head
    if '/t/' in head:
        data_t[cate] = head

for it in data_ent:
    fk_ent(it, data_ent[it])

print "    以下数据混有视频"

for it in data_t:
    fk_t(it, data_t[it])
