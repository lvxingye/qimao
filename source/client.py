# -*- coding:utf-8 -*-

import os

try :
    import winreg
except:
    pass

import get_book_adv
from search import search
from top_list import top

domain="https://www.qimao.com"
f=None

def scdstp(booklst):
    var=input("usage:number option [SaveDir=%%desktop]\noption:(d)ownload,(r)ead,(e)xit\n>>").split()
    while(var[0]!='exit'):
        if (var[0].lower() in "download"):
            print("Downloading...")
            try:
                f=open(var[2],"w")
            except IndexError:
                try:
                    deskpath=winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'),"Desktop")[0]
                    try:
                        list(os.scandir(deskpath+"\\qimao"))
                    except:
                        os.mkdir(deskpath+"\\qimao")
                    f=open(deskpath+"\\qimao\\"+booklst[int(var[1])][0]+".txt","w")
                except Exception as e:
                    raise 
            file=get_book_adv.parse_book(domain+booklst[int(var[1])][2])
            file.encode("utf-8")
            i=0
            while i<50:
                f.write(file[i*30000+1:(i+1)*30000+1])
            break
        if (var[0].lower() in "read"):
            pass
        var=input("usage:number option\noption:(d)ownload,(r)ead,(e)xit\n>>").split()

os.system("cls")
var=input("qimao_crawler\nusage:\n1--(s)earch keyword\n2--top boy|girl|book\ntip:boy:男生图书;  girl:女生图书;  book:出版图书\n>").split()
while(var[0]!='exit'):
    if(var[0] in 'top'):
        try :
            if (var[1]=='boy' or var[1]=='girl' or var[1]=='book'):
                booklst=top(var[1])
            else:
                raise SyntaxError
            for i in range(len(booklst)):
                print (i,'--',' '.join(booklst[i]))
            scdstp(booklst)
        except Exception as e:
            print("input error!")
    elif (var[0] in 'search'):
        try:
            booklst=search(var[1])
            for i in range(len(booklst)):
                print (i,'--',' '.join(booklst[i]))
            scdstp(booklst)
        except IndexError :
            print("input error!")
    else:
        print("input error!")
    var=input(">").split()
    
if not f:
    f.close()
