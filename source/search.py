# -*- coding:utf-8 -*-

import get_book_adv
import lxml.etree
import json
def search(wd):
    res=[]
    page=lxml.etree.HTML(get_book_adv.get_page(r"https://www.qimao.com/search/index/?keyword="+wd)).xpath("/html/body/div[4]/div/div/div[1]/div/div[1]/ul//li")
    title=[''.join(s.xpath('child::*//span[@class="s-tit"]//text()')) for s in page]
    author=[s.xpath('child::*//p[@class="p-bottom"]/span[1]/a/text()')[0] for s in page]
    tags=[''.join(s.xpath('child::*//span[@class="s-tags qm-tags clearfix"]//text()'))[40:-38] for s in page]
    urls=[s.xpath('div[3]/a/@href')[0] for s in page]
    for i in range(len(title)):
        res.append([title[i],author[i],urls[i],tags[i]])
    return res
if (__name__=="__main__"):
    print(json.dumps(search("局外人")))

