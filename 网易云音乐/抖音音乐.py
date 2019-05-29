# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 08:54:35 2019

@author: Administrator
"""

#from selenium import webdriver
#driver = webdriver.PhantomJS()
#driver.get("http://www.baidu.com")
#driver.save_screenshot("baidu.png")

from selenium import webdriver

import urllib
import requests
import os

BASE_DIR = os.getcwd()

class MusicSpider:
    def __init__(self):
        self.start_url = "https://music.163.com/discover/toplist?id=2250011882"#抖音歌单
        #self.start_url = "https://music.163.com/playlist?id=2643234673"#2019热歌排行榜
        #实例化浏览器
        self.driver = webdriver.Chrome()
        self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
                }
             
    def get_content_list(self):
        
        tr_list = self.driver.find_elements_by_xpath("//div[@class='j-flag']//tbody/tr")
        content_list=[]
        for tr in tr_list:
            item = {}
            item["download_url"]="http://music.163.com/song/media/outer/url?id={}.mp3".format(tr.find_element_by_xpath(".//div[@class='tt']/span").get_attribute("data-res-id"))
            item["song_name"] = tr.find_element_by_xpath(".//b").get_attribute("title")
            item["song_name"] = "".join([i.replace("/","") for i in item["song_name"]]) 
            item["song_auth"] = tr.find_element_by_xpath(".//div[@class='text']").get_attribute("title")
            item["song_auth"] = "".join([i.replace("/","") for i in item["song_auth"]]) 
            print(item)
            content_list.append(item)
           
        return content_list
        
    
    def download(self,content_list):
        for content in content_list:
            url = content["download_url"]
            song_name = content["song_name"]
            song_auth = content["song_auth"]
            response = requests.get(url,headers=self.headers,allow_redirects=False)
            new_url = response.headers["location"]
            
            filename =r"{}-{}.mp3".format(song_name,song_auth)
            path = os.path.join(BASE_DIR,filename)
            
            urllib.request.urlretrieve(new_url,path)  
            
           
    
    def run(self):
        #实现主要逻辑
        #1start_url
        #2发送请求，获取响应
        self.driver.get(self.start_url)
        self.driver.switch_to.frame("g_iframe")
        #3提取歌曲download_url song——name song-auth
        content_list = self.get_content_list()
        #4拼接url访问歌曲下载页面
        
        #5保存歌曲
        self.download(content_list)
        
        
if __name__ == '__main__':
    m=MusicSpider()
    m.run()        