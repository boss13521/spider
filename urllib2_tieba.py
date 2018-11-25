#coding=utf-8

import urllib2
import urllib

def loadPage(url,filename):
    """
    作用：根据url发送请求，获取服务器请求
    url：需要爬取的url地址
    filename:处理的人件名
    """
    print('正在下载'+filename)
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36i"}
    request=urllib2.Request(url,headers=headers)
 
    return urllib2.urlopen(request).read()

def writePage(html,filename):
    """
    作用：将html内容写入到本地
    html：服务器相应文件内容
    """
    print "正在保存"+filename
    #文件的写入
    with open(filename,"w")as f:
        f.write(html)

    print("*")*30

def tiebaSpider(url,b,e,fn):
    """
    作用：贴吧爬虫调度器，负责组合处理每个页面的url
    url：贴吧url的前半部
    beginpage：起始页
    endpage：终止页
    """
    for page in range(b,e+1):
        pn =(page-1)*50
        fullurl =url +"&pn="+str(pn)
#       print fullurl
        filename =str(fn)+"贴吧的第"+str(page)+"页.html"
        html=loadPage(fullurl,filename)
        writePage(html,filename)

if __name__ == "__main__":
    kw = raw_input("请输入需要爬取的贴吧名：")
    beginPage = int(raw_input("请输入起始页: "))
    endPage = int(raw_input("请输入终止页："))
    fn = kw

    url="http://tieba.baidu.com/f?"
    key=urllib.urlencode({"kw":kw})
    fullurl =url+ key
    #print(kw)
    tiebaSpider(fullurl,beginPage,endPage,fn)

    print"欢迎下次使用！！！"


















#url="http://www.baidu.com/"")
