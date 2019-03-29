#-------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# Name:        模块1
# Purpose:
#
# Author:      li
#
# Created:     28/12/2016
# Copyright:   (c) li 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def substitute():
    start=int(input("change a word from article No.:"))
    stop=int(input("to article No.:"))

    while input('continue?(No:0000):')!='0000':
        print('\n')
        origin=input('original word?:')
        new=input('change to?:')
        for i in range(start,stop+1):
            f1=open('corpus/'+repr(i)+'-std.txt','r',encoding='UTF-8')
            std=f1.read()
            count=std.count(origin)
            if count!=0:
                std2=std.replace(origin,new)
                print("第{0}篇替换了{1}个'{2}'，换成了“{3}”；".format(i,count,origin,new))
                f2=open('corpus/'+str(i)+'-std.txt','w',encoding='UTF-8')
                f2.write(std2)
                f2.close()
            f1.close()


def main():
    def getdate():
        import time
        date_str=time.asctime()
        date_str=date_str[4:10]+date_str[-5:]
        return date_str
    date_str=getdate()

    def initial():
        ver_file=open('./dict/latest.log','r',encoding='UTF-8')
        ver=ver_file.readline()
        ver=ver.replace('\n','')
        url_file=open('./dict/'+ver[:-3]+'log','r',encoding='UTF-8')
        urls=url_file.readlines()
        global urls
        url_file.close()

        url_file=open('./dict/'+ver[:-3]+'log','w',encoding='UTF-8')
        url_file.write('')
        url_file.close()

        dic_file=open('./dict/'+ver,'w',encoding='UTF-8')
        dic_file.write('')
        dic_file.close()

    initial()

    import dictionary as d


    def Add_to_dictionary():
        print('现在开始执行Add_to_dictionary()')
        def output_to_dict(dic,url_list):
            def freshdict(dic,file_str):
                    '''This output dic into a .dic file'''
                    def format_fix(fix_dict):# for Prefix and Suffix
                            ret=''
                            for ele in fix_dict.keys():
                                    ret=ret+ele+':'+str(fix_dict[ele])+','
                            return ret
                    f=open(file_str,'w',encoding='UTF-8')
                    for entry in dic:
            #中文|Word|360|Num|简体:290,繁体:60,None:10|Pre|分词:230,自修:100,考试:20,None:10|Suf|
                            f.write("{0}|Word|{1}|Num|{2}|Pre|{3}|Suf|\n"
                                    .format(entry['Word'],entry['Num'],format_fix(entry['Pre']),format_fix(entry['Suf'])))
                    f.close()


            def freshurl(url_list,file_str):
                    """This output new_url_list into a .log file"""
                    f=open(file_str,'w',encoding='UTF-8')
                    for ele in url_list:
                        if ele not in urls:
                            f.write(ele)
                    f.writelines(urls)
                    f.close()
   #Refresh Version Information
            f=open("dict/latest.log","w")

            file_str=date_str+'.dic'
            f.write(file_str+'\n')
            f.close()
            freshdict(dic,"dict/"+file_str)


        start=int(input("""Now we add words in ariticles into a fresh dict!
Start:"""))
        stop=int(input("Stop:"))

        for i in range(start,stop+1):
            dic,url_list=d.getdict()
            d.train_one_passage(dic,url_list,text_str='corpus/'+repr(i)+'-std.txt')
            d.output_to_dict(dic,url_list)


    Add_to_dictionary()

substitute()
main()