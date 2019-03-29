#-------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# Name:        模块1
# Purpose:
#
# Author:      li
#
# Created:     29/12/2016
# Copyright:   (c) li 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def main():
    while True:
        i=input('number?')
        if i=='0000':
            break
        type=input('type?(fmm,std,stat)')
        if type!='':
            f_ansi=open('corpus/'+i+'-'+type+'.txt','r')
            ff=f_ansi.readlines()
            f_ansi.close()
            f_utf=open('corpus/'+i+'-'+type+'.txt','w',encoding='utf-8')
        else:
            f_ansi=open('corpus/'+i+'.txt','r')
            ff=f_ansi.readlines()
            f_ansi.close()
            f_utf=open('corpus/'+i+'.txt','w',encoding='utf-8')
        f_utf.writelines(ff)
        f_utf.close()
        f_ansi.close()

main()