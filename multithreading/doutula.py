#coding=utf-8
import requests
import urllib
import re
import threading

from lxml import etree
from fake_useragent import UserAgent
from tqdm import tqdm

def parse_url(url):
    headers = {
        'user-agent':UserAgent().random
    }
    response = requests.get(url,headers=headers)
    html_str = response.content.decode()
    html = etree.HTML(html_str)
    # print(type(html))
    img_list = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
    # title_list = html.xpath("//div[@class='page-content text-center']//img/@alt")

    for img in tqdm(img_list):
        images = img.xpath("./@data-original")[0]
        title = img.xpath("./@alt")[0]
        title = re.sub(r'[\？，！…]','',title)
        suffix = images[-4:]
        # print(images)
        # print(title)
        # print(suffix)
        filename = title + suffix
        # print(filename)
        urllib.request.urlretrieve(images,'images/'+filename)

def main():

    #https: // www.doutula.com / photo / list /?page = 2
    for i in range(5):
        url = "https://www.doutula.com/photo/list/?page={}".format(i)
        parse_url(url)

if __name__ == '__main__':
    main()