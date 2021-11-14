import requests as rq
import re
from bs4 import BeautifulSoup as bs
import json

#获取加密参数.解析算法均来自：一只不会爬的虫（csdn）
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
def get_page(url,user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31",proxy=""):
    """
    url:爬取网址；user-agent:爬虫ua;proxy:爬虫代理；
    此函数仅适用于七猫！！！
    """
    headers={
    "User-Agent":user_agent
    }
    #一次请求
    page=rq.get(url,headers=headers)
    #获取加密参数
    arg1 = re.findall("arg1=\'(.*?)\'", page.content.decode())[0]
    s1 = get_unsbox(arg1)
    _0x4e08d8 = "3000176000856006061501533003690027800375"
    _0x12605e = get_hexxor(s1, _0x4e08d8)
    #二次请求
    headers["cookie"]="acw_sc__v2=%s" % _0x12605e
    page=rq.get(url,headers=headers)
    return page.content.decode()

def parse_chap(contant):
    """
    解析当前章节
    """
    res_json=json.loads(contant)
    soup=bs(res_json["chapter"]["chapter_content"],"lxml")
    text=""
    for i in soup.body:
        if i.string:
            text+=str(i.string)
    res=json.loads(res_json["next_chapter_info"])
    return {
        "text":text,
        "title":res_json["chapter"]["title"],
        "next":[res["book_id"],res["chapter_id"],res["is_final"]] #bookid,chapid,isfinished
    }

def get_first_chap(contant):
    """
    获取首页及book_id,chapter_id
    """
    soup=bs(contant,"lxml")
    chap2_info=json.loads(str(soup.body.script.string)[27:-2])
    return parse_chap(get_page("https://www.qimao.com/shuku/{book_id}-{chap_id}-1-0/".format(book_id=chap2_info["book_id"],chap_id=str(int(chap2_info["chapter_id"])-1))))

def get_info(contant):
    """
    封面url demo:https://www.qimao.com/shuku/156846/
    返回书本信息：作者，来源，字数，标签...
    """
    book_info=bs(contant,"lxml").find(name="div",attrs={"class":"data-txt"})
    tags=[]
    for i in list(book_info.find("p",{"class":"p-tags"}).span.children)[2:]:
        if i != '\n':
            tags.append(i.string)
    return {
        "book_name":str(book_info.div.h2.string),
        "author_name":str(book_info.find("p",{"class":"p-name"}).a.string),
        "wd_count":str(book_info.find("p",{"class":"p-num"}).span.get_text()),
        "is_finished":(str(book_info.find("p",{"class":"p-tags"}).em.string)=="完结"),
        "tags":tags
    }

def parse_book(book_url,ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31",proxy=""):
    """
    封面url demo:https ://ww w.qim ao.co m/shu ku/156846/
    通过封面url解析/下载全书文字
    """
    book_info=get_info(get_page(book_url))
    #
    contant=book_info["book_name"]+"\n\n\n作者："+book_info["author_name"]+"\n字数："+book_info["wd_count"]+"\n\n"
    for i in book_info["tags"]:
        contant+=i+' '
    contant+="\n小说来自七猫中文网\n\n------------------------------------\n\n"
    #
    chap=get_first_chap(get_page(r"https://www.qimao.com/reader/index/"+book_url[28:-1]+'/',user_agent=ua,proxy=proxy))
    contant+=chap["title"]+'\n'+chap["text"]+"\n\n"
    while(chap["next"][1]):
        #print("get chap "+chap["next"][1]+"\n")
        chap=parse_chap(get_page("https://www.qimao.com/shuku/{bid}-{cid}-1-0/".format(bid=chap["next"][0],cid=chap["next"][1]),user_agent=ua,proxy=proxy))
        contant+=chap["title"]+'\n'+chap["text"]+"\n\n"
    return contant

import os
f=open(r"C:\Users\lvxy\1.txt","w+")
f.write(parse_book("https://www.qimao.com/shuku/161692/"))
f.close()