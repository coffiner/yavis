#!/usr/bin/python
# -*- coding: utf-8 -*-  

# F**k off huya !!!
# By Jack
# 2016年 04月 10日 星期日 23:23:47 CST

import urllib2 as ul, re, json, time

data_url = 'http://www.huya.com/index.php?m=Game&do=ajaxGameLiveByPage&gid=GID&page=PAGE'
print ','.join(['分类','时间','直播数目','在线人数'])

# check index
index = 'http://www.huya.com/index'
html = ul.urlopen( ul.Request(index) ).read()
start = html.find('全部分类')
end = html.find('下载客户端')
html = html[start:end]
gid_par = re.compile(r'(?<=huya.com/g/)100\d+(?=")', re.X)
cat_par = re.compile(r'(?<=tle-span">).*?(?=</span)', re.X)

gid_match_group = gid_par.search(html)
# lets go into each gid
while gid_match_group:
    end = gid_match_group.end()
    html = html[end:]
    cat_match_group = cat_par.search(html)
    gid = gid_match_group.group()
    cat = cat_match_group.group()
    gid_match_group = gid_par.search(html)
    
    #print gid, cat
    json_data = ul.urlopen( ul.Request(data_url.replace('GID',gid)) ).read()
    json_data = json.loads(json_data)
    #print json_data
    total = json_data['data']['total']
    sum = 0
    page = 0
    people = 0
    start_time = time.ctime()
    while True:
        page += 1
        url = data_url
        url = url.replace('GID',gid).replace('PAGE',str(page))
        json_data = ul.urlopen( ul.Request(url)).read()
        #time.sleep(0.02)
        json_data = json.loads(json_data)
        total = json_data['data']['total']
        list = json_data['data']['list']
        if not list:
            break
        for item in list:
            sum += 1
            people += int(item['totalCount'])
    print ','.join([cat, start_time, str(sum), str(people)])

