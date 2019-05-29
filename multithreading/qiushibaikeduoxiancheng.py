# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 09:21:51 2019

@author: Administrator
"""
from queue import Queue

from lxml import etree

import requests
import json
import threading

class QiushiSpider:
    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/hot/page/{}/"
        self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
                }
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()
        
    def get_url_list(self):
        
        #return [self.url_temp.format(i) for i in range(1,14)]
        for i in range(1,14):
            self.url_queue.put(self.url_temp.format(i))
    
    def parse_url(self):
        while True:
            url = self.url_queue.get()
            print(url)
            response = requests.get(url, headers=self.headers)
            #return response.content.decode()
            self.html_queue.put(response.content.decode())
            self.url_queue.task_done()
            
    def get_content_list(self):
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            #div_list = html.xpath("//div[@class="content"]/span[1]/text()")
            div_list = html.xpath('//div[@id="content-left"]/div')#分组
            content_list = []
            for div in div_list:
                item = {}
                item["content"] = div.xpath('.//div[@class="content"]/span[1]/text()')
                item["content"] = [i.replace("\n","") for i in item["content"]]
                content_list.append(item)
            
            #return content_list
            self.content_queue.put(content_list)
            self.html_queue.task_done()
            
    def save_content_list(self):
        while True:
            content_list = self.content_queue.get()
            with open("qiushiduoxianc.text","a",encoding="utf-8") as f:
                for i in content_list:
                    f.write(json.dumps(i,ensure_ascii=False))
                    f.write("\n")
                    
            self.content_queue.task_done()
    def run(self):#主要逻辑
        thread_list = []
        #1start-url
        t_url = threading.Thread(target=self.get_url_list)
        thread_list.append(t_url)
        
        #2遍历url——list 发送请求，获取响应
        t_html = threading.Thread(target=self.parse_url)
        thread_list.append(t_html)
        #3提取数据，获取下一页url
        t_content = threading.Thread(target=self.get_content_list)
        thread_list.append(t_content)
        #4保存
        
        t_save = threading.Thread(target=self.save_content_list)
        thread_list.append(t_save)
        
        for i in thread_list:
            i.setDaemon(True)#子线程设置为守护线程，主线程结束停止。
            i.start()
            
        for q in [self.url_queue,self.html_queue,self.content_queue]:
            q.join()#主线程等待队列的任务完成后再结束
        print("下载完成")
    
     
    
if __name__ =='__main__':
    q=QiushiSpider()
    q.run()