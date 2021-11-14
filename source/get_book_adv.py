import requests as rq
import re
from lxml import etree as tr
import json
import threading
import time

headers={}

url_queue=[]     #多线程
chap_contant={}
threads={}
domin="https://www.qimao.com"


#获取加密参数.解析算法均来自：一只不会爬的虫（csdn）
#原文url:https://blog.csdn.net/weixin_40352715/article/details/107965137
def get_unsbox(arg1):
    _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd,                 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c,                 0x22, 0x25, 0xc, 0x24]
    _0x4da0dc = []
    _0x12605e = ''
    for i in _0x4b082b:
        _0x4da0dc.append(arg1[i-1])
    _0x12605e = "".join(_0x4da0dc)
    return _0x12605e
def get_hexxor(s1, _0x4e08d8):
    _0x5a5d3b = ''
    for i in range(len(s1)):
        if i % 2 != 0: continue
        _0x401af1 = int(s1[i: i+2], 16)
        _0x105f59 = int(_0x4e08d8[i: i+2], 16)
        _0x189e2c_10 = (_0x401af1 ^ _0x105f59)
        _0x189e2c = hex(_0x189e2c_10)[2:]
        if len(_0x189e2c) == 1:
            _0x189e2c = '0' + _0x189e2c
        _0x5a5d3b += _0x189e2c
    return _0x5a5d3b


#获取网页
def get_page(url,cookies=None,user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31",proxy=""):
    """
    url:爬取网址；user-agent:爬虫ua;proxy:爬虫代理；
    此函数仅适用于七猫！！！
    """
    if cookies:
        headers["cookie"]=cookies
    try:
        headers["cookie"]
    except:
        headers["User-Agent"]=user_agent
        #一次请求。获取cookies
        page=rq.get(url,headers=headers)
        #获取加密参数
        #原文url：https://blog.csdn.net/weixin_40352715/article/details/107965137
        arg1 = re.findall("arg1=\'(.*?)\'", page.content.decode())[0]
        s1 = get_unsbox(arg1)
        _0x4e08d8 = "3000176000856006061501533003690027800375"
        _0x12605e = get_hexxor(s1, _0x4e08d8)
        headers["cookie"]="acw_sc__v2=%s" % _0x12605e
    #二次请求
    page=rq.get(url,headers=headers)
    return re.sub(r"(\&nbsp;)",' ',page.content.decode())

def parse_chap(contant):
    """
    解析当前章节
    """
    res_json=json.loads(contant)
    text=re.sub("</?p>","",res_json['chapter']['chapter_content'])
    return {
        "text":text,
        "title":res_json["chapter"]["title"]
    }

'''def get_first_chap(contant):
    """
    获取首页及book_id,chapter_id
    """
    tree=tr.HTML(contant)
    chap2_info=json.loads(tree.xpath(r"/html/body/script[1]/text()")[0][27:-2])
    return parse_chap(get_page("https://www.qimao.com/shuku/{book_id}-{chap_id}-1-0/".format(book_id=chap2_info["book_id"],chap_id=(int(chap2_info["chapter_id"])-1))))
'''
def get_info(contant):
    """
    封面url demo:https://www.qimao.com/shuku/156846/
    返回书本信息：作者，来源，字数，标签...
    """
    book_info=tr.HTML(contant).xpath('//div[@class="data-txt"]')[0]
    tags=book_info.xpath('//p[@class="p-tags"]//a//text()')
    
    return {
        "book_name":(book_info.xpath('//h2/text()')[0]),
        "author_name":(book_info.xpath('//p[@class="p-name"]//a/text()')[0]),
        "wd_count":(book_info.xpath('//p[@class="p-num"]//span//text()')[0]),
        "is_finished":((book_info.xpath('//p[@class="p-tags"]//em//text()')[0])=="完结"),
        "is_vip":book_info.xpath('/html/body/div[3]/div[2]/div/div[1]/div/dl[2]/dd/div[1]/span[last()]//*')[-1].tag=='i',
        "tags":tags
    }

def get_contant_url_list(contant):
    """获取内容url列表"""
    tree=tr.HTML(contant)
    return tree.xpath("/html/body/div[3]/div[2]/div/div[1]/div/dl[2]/dd/div[1]//a/@href")

def mythread(ua,lnk):
    chap=parse_chap(get_page("%s%s-1-0/"%(domin,lnk[:-1]),None,ua))
    #print(lnk)
    chap_contant[lnk]=chap

def parse_book(book_url,ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31",proxy=""):
    """
    封面url demo:https://www.qimao.com/shuku/156846/
    通过封面url解析/下载全书文字
    """
    t=time.process_time()
    cover=get_page(book_url,None,ua)
    book_info=get_info(cover)
    #
    if book_info["is_vip"]:
        return "vip"
    contant=book_info["book_name"]+"\n\n\n作者："+book_info["author_name"]+"\n字数："+book_info["wd_count"]+"\n\n"
    for i in book_info["tags"]:
        contant+=i+' '
    contant+="\n小说来自七猫中文网\n\n------------------------------------\n\n"
    #
    url_queue=get_contant_url_list(cover)
    
    for i in url_queue:
        thread=threading.Thread(target=mythread,args=(ua,i),name=i)
        #thread.setDaemon(True)
        thread.start()
        threads[i]=thread
        time.sleep(0.1)
    for i in url_queue:
        try:
            contant+=chap_contant[i]["title"]+"\n"+chap_contant[i]["text"]
        except KeyError:
            threads[i].join()
            contant+=chap_contant[i]["title"]+"\n"+chap_contant[i]["text"]
    print("Finished!\nTime:",time.process_time()-t)
    return contant
if __name__=="__main__":
    t=time.process_time()
    parse_book(input())
    print(time.process_time()-t)
