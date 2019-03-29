#-------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# Name:        模块1
# Purpose:
#
# Author:      li
#
# Created:     27/12/2016
# Copyright:   (c) li 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def main():

    start=int(input("start:"))
    stop=int(input("stop:"))

    while True:
        print('\n')
        origin=input('original word?:')
        if origin=='0000':break
        new=input('change to?:')
        for i in range(start,stop+1):
            f1=open('corpus/'+str(i)+'-std.txt','r',encoding='UTF-8')
            std=f1.read()
            count=std.count(origin)
            if count!=0:
                std2=std.replace(origin,new)
                print("第{0}篇替换了{1}个'{2}'".format(i,count,origin))
                f2=open('corpus/'+str(i)+'-std.txt','w',encoding='UTF-8')
                f2.write(std2)
                f2.close()
            f1.close()


main()