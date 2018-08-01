# -*- coding: utf-8 -*-

# 基于tornado的并发爬虫测试代码，用于测试是否有反爬或者ban ip机制

import requests
import time
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPError, HTTPRequest
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.log import gen_log
# from tornado.curl_httpclient import CurlAsyncHTTPClient

# 从txt中读取urls
urls = []
openFile = open("./urls.txt")
for line in openFile:
    urls.append(line.strip())
print("urls added in completed.")


Headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# 下载页面
# def download_page(url):
#     response = requests.get(url, Headers, timeout=10)
#     print("download page status_code: " + str(response.status_code))
#     response.encoding = 'utf-8'
#     if response.status_code == 200:
#         content = response.content
#         response.close()
#         return content
#     else:
#         return None

# 将html写入文件
def out_HTML(filename, HTML):
    with open(filename, 'wb') as f:
        f.write(HTML)
    f.close()

# # 抓取并输出文件
# def crawl_outputFile():
#     count = 0
#     for url in urls:
#         print(count)
#         html = download_page(url)
#         outFilename = "./html/" + str(count) + "_data.html"
#         count += 1
#         out_HTML(outFilename, html)

count = 0
# class NoQueueTimeoutHTTPClient(SimpleAsyncHTTPClient):
#     def fetch_impl(self, request, callback):
#         key = object()
#         self.queue.append((key, request, callback))
#         self.waiting[key] = (request, callback, None)
#         self._process_queue()
#         if self.queue:
#             gen_log.debug("max_clients limit reached, request queued. %d active, %d queued requests." % (len(self.active), len(self.queue)))
class MyClass(object):
    count = 0
    def __init__(self):
        # AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
        self.http = AsyncHTTPClient()

    @coroutine  
    def get(self, url):
        #tornado会自动在请求首部带上host首部        
        request = HTTPRequest(url=url,
                            method='GET',
                            headers=Headers,
                            connect_timeout=2.0,
                            request_timeout=2.0,
                            follow_redirects=False,
                            max_redirects=False,
                            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",)
        # yield self.http.fetch(request, callback=self.find, raise_error=False)
        yield self.http.fetch(request, self.find)

    def find(self, response):
        global count
        if response.error:
            print(response.error)
        # print(type(response.body))
        outFilename = "./html/" + str(count) + "_data.html"
        out_HTML(outFilename, response.body)
        print(count, response.code, response.effective_url, response.request_time)
        count += 1

class Download(object):

    def __init__(self):
        self.a = MyClass()
        self.urls = urls
    @coroutine
    def d(self):
        print(u'基于tornado的并发抓取')        
        t1 = time.time()
        for url in self.urls:
            response = self.a.get(url)
            yield response
        t = time.time() - t1
        print(t)
        
if __name__ == '__main__':
    
    dd = Download()
    loop = IOLoop.current()
    loop.run_sync(dd.d)