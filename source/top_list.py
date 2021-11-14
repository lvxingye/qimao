# -*- coding:utf-8 -*-

import get_book_adv
import lxml.etree
import re
def top(type):
    res=[]
    lst=lxml.etree.HTML(get_book_adv.get_page(r'https://www.qimao.com/paihang/')).xpath('//div[@list-type="%s"]/ul//ul//li'%type)
    title=[''.join(s.xpath('div[2]/span[1]/a/text()')) for s in lst]
    author=[s.xpath('div[2]/span[2]/a/text()')[0] for s in lst]
    urls=[s.xpath('div[2]/span[1]/a/@href')[0] for s in lst]
    for i in range(len(title)):
        res.append([title[i],author[i],urls[i]])
    return res
