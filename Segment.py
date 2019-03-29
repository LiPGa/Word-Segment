from ss import fmm
from ss import stat2 as stat
from ss import stat_opt
from ss import dp_opt
from ss import final
import dictionary
# -*- coding: utf-8 -*-

def use_fmm(s1,dic,url,index):
    result_str=fmm.segment(s1,dic)

    f=open('corpus/'+repr(index)+'-fmm.txt','w',encoding='UTF-8')
    f.write(url)
    f.write(result_str)

    f.close()

def use_stat(s1,dic,url,index):
    result_str=stat.stat_seg(s1,dic)
    f=open('corpus/'+repr(index)+'-stat.txt','w',encoding='UTF-8')
    f.write(url)
    f.write(result_str)

    f.close()

def use_stat_opt(s1,dic,url,index):
    result_str=stat_opt.stat_seg(s1,dic)
    f=open('corpus/'+repr(index)+'-stat_opt.txt','w',encoding='UTF-8')
    f.write(url)
    f.write(result_str)

    f.close()

def use_dp_opt(s1,dic,url,index):
    result_str=dp_opt.segment(s1,dic)
    f=open('corpus/'+repr(index)+'-dp_opt.txt','w',encoding='UTF-8')
    f.write(url)
    f.write(result_str)

    f.close()

def use_final(s1,dic,url,index):
    result_str=final.segment(s1,dic)
    f=open('corpus/'+repr(index)+'-final.txt','w',encoding='UTF-8')
    f.write(url)
    f.write(result_str)

    f.close()

import sys
import os
sys.path.append(os.path.abspath('.'))

if __name__=='___main__':
    start=int(input("start:"))
    stop=int(input("stop:"))
    ##start=10
    ##stop=10
    for i in range(start,stop+1):
        f=open('corpus/'+repr(i)+'.txt','r',encoding='UTF-8')
        url=f.readline()#Remove the URL in head
        s1=f.read()
        f.close()
        dic,url_list=dictionary.getdict()
    ##    use_fmm(s1,dic,url,i)
    ##    use_stat(s1,dic,url,i)
    ##    use_stat_opt(s1,dic,url,i)
    ##    use_dp_opt(s1,dic,url,i)
        use_final(s1,dic,url,i)

