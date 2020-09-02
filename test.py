"""分页请求stackexchange的api获得所有问题信息"""
from urllib.error import HTTPError
import random
import urllib.request
import datetime
import json
import socket
from io import BytesIO
import gzip

import sqlutil

if __name__ == '__main__':
    """"""
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
    pageindex = 1
    socket.setdefaulttimeout(120)
    retrytime = 5
    while 1:
        url = 'http://api.stackexchange.com/questions?page={index}&pagesize=100&site=codereview'.format(index = pageindex)#依次分页访问
        req = urllib.request.Request(url,headers = headers)
        try:
            for i in range(retrytime):
                try:
                    # 随机选择一个代理
                    proxy = random.choice(proxy_list)
                    httpproxy_handler = urllib.request.ProxyHandler(proxy)
                    opener = urllib.request.build_opener(httpproxy_handler)
                    res = opener.open(req)
                    if res.code == 200:
                        break
                except Exception as e:
                    print(e)
                    print("retrying...",i)
        except HTTPError:
            print("end")
            break
        else:
            response = res.read()
            buff = BytesIO(response)
            f = gzip.GzipFile(fileobj = buff)
            htmls = f.read().decode('utf-8')
            results = json.loads(htmls)
            for item in results['items']:
                if ('user_id' in item['owner']):
                    owner_id=item['owner']['user_id']             # 提问者id
                    owner_reputation=item['owner']['reputation']  # 提问者声誉
                    view_count=item['view_count']                 # 问题访问次数
                    answer_count=item['answer_count']             # 回答个数
                    score=item['score']                           # 问题评分
                    question_id=item['question_id']               # 问题id
                    title=item['title']                           # 问题标题
                    sqlutil.addaQuestionRecord(owner_id,owner_reputation,view_count,answer_count,score,question_id,title)
            print("get",pageindex)
            pageindex += 1
