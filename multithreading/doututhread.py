# coding=utf-8
import requests
import urllib
import re
import threading
import os
import time

from lxml import etree
from fake_useragent import UserAgent
from tqdm import tqdm
from queue import Queue


class ImageSpider:
    def __init__(self):
        self.url_temp ="https://www.doutula.com/photo/list/?page={}"
        self.headers ={
            'user-agent': UserAgent().random
                        }
        self.html_queue = Queue()
        self.url_queue = Queue()
        self.content_queue = Queue()

    def get_url(self):
        #第一次请求
        for i in range(10):
            url = self.url_temp.format(i)
            self.url_queue.put(url)

    def parse_url(self):

        #进入循环请求
        while True:
            url=self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            html_str = response.content.decode()
            # return html_str
            self.html_queue.put(html_str)
            self.url_queue.task_done()


    def get_content_list(self):
        while 1:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            # print(type(html))
            #分组
            img_list = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
            # title_list = html.xpath("//div[@class='page-content text-center']//img/@alt")
            next_url = html.xpath("//a[@rel='next']/@href")[0]
            next_url = "https://www.doutula.com" + next_url

            self.url_queue.put(next_url)

            # next_url = html.xpath("//a[contains(text(),'>')]/@href")
            # print(next_url)
            content_list = []
            for img in img_list:
                item = {}
                item["images"] = img.xpath("./@data-original")[0]
                item["title"] = img.xpath("./@alt")[0]
                item["title"] = re.sub(r'[\？，！…]', '', item["title"])
                item["suffix"] = item["images"][-4:]
                content_list.append(item),next_url

            # return content_list
            self.content_queue.put(content_list)
            self.html_queue.task_done()
    def save_content(self):
        while 1:
            content_list = self.content_queue.get()
            for content in tqdm(content_list):
                images = content["images"]
                title = content["title"]
                suffix = content["suffix"]
                filename = title + suffix
                # print(filename)
                #保存数据
                urllib.request.urlretrieve(images, "doutuimages/"+filename )
            self.content_queue.task_done()
    def main(self):#实现主逻辑
        #1start——url
        # print("11122112")
        # #2发送请求，获取相应
        # self.first_parse_url()
        # print("11122112")
        # #3获取数据,获取下一页url
        # self.get_content_list()
        # # print(content_list)
        # #保存数据
        # self.save_content()
        # print("111111111111")
        #请求下一页，进入循环
        # threading_list = []
        t= threading.Thread(target=self.get_url)
        t.setDaemon(True)
        t.start()
        for i in range(3):
            t1 =threading.Thread(target=self.parse_url)
            t1.setDaemon(True)
            t1.start()
        for i in range(2):
            t2 =threading.Thread(target=self.get_content_list)
            t2.setDaemon(True)
            t2.start()
        for i in range(3):
            t3 = threading.Thread(target=self.save_content)
            t3.setDaemon(True)
            t3.start()
        # time.sleep(1)
        for q in [self.content_queue,self.html_queue,self.url_queue]:
            q.join()
        print("下载完成")
if __name__ == '__main__':
    i=ImageSpider()
    i.main()