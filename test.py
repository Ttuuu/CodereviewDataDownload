"""
@author: ttu
因为校园网半夜断网 所以数据库里设置了vis字段判断该问题是否已经爬过 避免重复访问
    owner_id：提问者id
    owner_reputation：提问者声誉
    view_count：问题访问次数
    answer_count：回答个数
    score：问题评分
    question_id：问题id
    title：问题标题

网站根据ip来ban请求
虽然设置了代理 不过没用到
"""
from urllib.request import urlopen
from urllib.request import Request
import urllib
import random
import urllib.request
import datetime
import json
import socket

import sqlutil

from io import BytesIO
import gzip
 
if __name__ == '__main__':
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
               'Content-Type':'application/json',
               'Accept':'application/json',
               'Connection':'close',
               }
    proxy_list = [
        {"http":"http://196.54.50.143:80"},
        {"http":"http://207.154.231.213:3128"},
        {"http":"http://138.68.41.90:8080"},
        {"http":"http://221.182.31.54:8080"},
        {"http":"http://101.37.118.54:8888"},
        {"http":"http://101.37.118.54:8888"},
        {"http":"http://120.79.209.11:3128"},
        {"http":"http://118.69.50.154:80"},
        {"http":"http://121.102.2.141:80"},
        {"http":"http://61.135.186.243:80"},
        {"http":"http://59.120.117.244:80"},
        {"http":"http://218.59.139.238:80"}
    ]
    proxy = random.choice(proxy_list)
    httpproxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(httpproxy_handler)
    res = opener.open(Request("https://www.baidu.com/",headers=headers))
    print("test end")  #测试一下网络
    
    pageindex=1
    socket.setdefaulttimeout(120)
    retrytime=5
    while 1:
        url = 'https://api.stackexchange.com/questions?page={index}&pagesize=100&site=codereview'.format(index=pageindex)#依次分页访问
        req = Request(url,headers=headers)
        testflag=False
        try:
            for i in range(retrytime):
                try:
                    # 随机选择一个代理
                    proxy = random.choice(proxy_list)
                    httpproxy_handler = urllib.request.ProxyHandler(proxy)
                    opener = urllib.request.build_opener(httpproxy_handler)
                    res = opener.open(req)
                    testflag=True
                    if res.code==200:
                        break
                except Exception as e:
                    print(e)
                    print("retrying...",i,"testflag",testflag)
        except urllib.error.HTTPError:
            print("end")
            break
        else:
            response = res.read()
            buff = BytesIO(response)
            f = gzip.GzipFile(fileobj=buff)
            htmls = f.read().decode('utf-8')
            results=json.loads(htmls)

            for item in results['items']:
                if ('user_id' in item['owner']):
                    owner_id=item['owner']['user_id']
                    owner_reputation=item['owner']['reputation']
                    view_count=item['view_count']
                    answer_count=item['answer_count']
                    score=item['score']
                    question_id=item['question_id']
                    title=item['title']
                    sqlutil.addaQuestionRecord(owner_id,owner_reputation,view_count,answer_count,score,question_id,title)
            print("read a record",pageindex,"quota remain",results['quota_remaining'])#显示当前ip剩余次数
            pageindex+=1
