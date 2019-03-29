#-------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# Name:        模块1
# Purpose:
#
# Author:      li
#
# Created:     22/12/2016
# Copyright:   (c) li 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def rating(raw_infilename,std_infilename):
    import string
    import re
    score=100
    punctuation=string.punctuation
    chnpunctuation='，。、？！……：；“‘”’{}【】《》——（）'


    def splitwords(text):
                #根据‘|’来分句
        text=text.replace('｜','|')
        if(text[0]!='|'):text='|'+text
        if(text[-1]!='|'):text=text+'|'
        text_list=list(text)

        char_list=[]
        for i in range(len(text_list)):
            char=text_list[i]
            if ((char in punctuation)and not(char=='|')):char_list.append('|')
            elif ((char=='\n')or(char=='　')or(char==' ')or(char=='\t')):pass
            elif (char in chnpunctuation):char_list.append('|')
            else:char_list.append(char)

        text=''.join(char_list)
        while ('||' in text):text=text.replace('||','|')

                        #Remove punctuation
        word_seq=text.split('|')
        word_num=len(word_seq)-2

        word_seq[0],word_seq[-1]='None','None'
        return(word_seq)
    raw_infile=open(raw_infilename,'r',encoding='utf-8')
    std_infile=open(std_infilename,'r',encoding='utf-8')
    (fa,fb)=('','')
    for line in raw_infile:
        fa+=''.join(re.split(r'[\s]*',line))
    for line in std_infile:
        fb+=''.join(re.split(r'[\s]*',line))
    sa,sb=splitwords(fa),splitwords(fb)
    concat_err,split_err,slide_err=[],[],[]
    #[{'|Word|':,'|Pre|':,'|Suf|':,'|Correct|':}]
    num_concat,num_split,num_slide=0,0,0


    for i in range (min(len(sa),len(sb))-1):
        if sa[i]!=sb[i]:
            if len(sa[i])<len(sb[i]) and len(sa[i+1])<len(sb[i]):
            #concat 多分了
                num_concat+=1
                for ii in range(i+1,len(sa)):
                    if ''.join(sa[i:ii+1])==sb[i]:
                        concat_err.append({'|WORD|':'|'.join(sa[i:ii+1]),'|Pre|':sb[i-1],'|Suf|':sb[i+1],'|Correct|':sb[i]})
                        sa[i]=sb[i]
                        del sa[i+1:ii+1]
                        break
            elif len(sa[i])>len(sb[i]) and len(sa[i])>len(sb[i+1]):
            #split 少分了 首|届
                num_split+=1
                for ii in range(i+1,len(sb)):
                    if ''.join(sb[i:ii+1])==sa[i]:
                        split_err.append({'|WORD|':sa[i],'|Pre|':sb[i-1],'|Suf|':sb[ii+1],'|Correct|':'|'.join(sb[i:ii+1])})
                        del sa[i]
                        sa[i:i]=sb[i:ii+1]
                        break
            elif (len(sa[i])<len(sb[i]) and len(sa[i+1])>=len(sb[i])):
            #slide,|分错地方的情况  e.g:领|导人→领导|人
            #服|务实|体|经济→服务|实体经济
                num_slide+=1
                slide_err.append({'|WORD|':'|'.join(sa[i:i+2]),'|Pre|':sb[i-1],'|Suf|':sb[i+2],'|Correct|':'|'.join(sb[i:i+2])})
                                            #服|务实 pre:如何 suf:仍然
                sa[i+1]=sa[i+1][len(sb[i])-len(sa[i]):]
                sa[i]=sb[i]

            elif(len(sa[i])>len(sb[i]) and len(sa[i])<=len(sb[i+1])):
            #e.g:各方|面→各|方面
            #我是|李聆嘉→我|是李|聆嘉???!!!!!!!!
                num_slide+=1
                slide_err.append({'|WORD|':'|'.join(sa[i:i+2]),'|Pre|':sb[i-1],'|Suf|':sb[i+2],'|Correct|':'|'.join(sb[i-1:i+2])})
                sa[i],sa[i+1]=sb[i],sb[i+1]

    score= float('%.1f'%(100-100*(num_concat+num_slide+num_split)/(len(sa)-1)))#计算正确率
    result= {'|SCORE|':score,'|concat|':num_concat,'|split|':num_split,'|slide|':num_slide}


    f4.write(raw_infilename[7:len(raw_infilename)-4])
    f4.write('\n')
    f4.write('score:{0}，concat:{1},split:{2},slide:{3},\n'.format(result['|SCORE|'],result['|concat|'],result['|split|'],result['|slide|']))

    f1.write("|Score|:{0},concat_err×{1}\n"
                                    .format(result['|SCORE|'],result['|concat|']))
    if concat_err==[]:
        f1.write('None')
    else:
        for ele in concat_err:
            f1.write("|WORD|:{0},|pre|:{1},|suf|:{2},|Correct|:{3}\n"
                                    .format(ele['|WORD|'],ele['|Pre|'],ele['|Suf|'],ele['|Correct|']))
    f2.write("|Score|:{0},split_err×{1}\n"
                                    .format(result['|SCORE|'],result['|split|']))
    if split_err==[]:
        f2.write('None')
    else:
        for ele in split_err:
            f2.write("|WORD|:{0},|pre|:{1},|suf|:{2},|Correct|:{3}\n"
                                    .format(ele['|WORD|'],ele['|Pre|'],ele['|Suf|'],ele['|Correct|']))
    f3.write("|Score|:{0},slide_err×{1}\n"
                                    .format(result['|SCORE|'],result['|slide|']))
    if slide_err==[]:
        f3.write('None')
    else:
        for ele in slide_err:
            f3.write("|WORD|:{0},|pre|:{1},|suf|:{2},|Correct|:{3}\n"
                                    .format(ele['|WORD|'],ele['|Pre|'],ele['|Suf|'],ele['|Correct|']))
    return

def rating_a_passage_stat(i):
    raw_infilename='corpus/'+str(i)+'-stat.txt'
    std_infilename='corpus/'+str(i)+'-std.txt'

    f1=open("corpus/stat-Concat_Error.log","a",encoding='utf-8')
    f2=open("corpus/stat-Split_Error.log","a",encoding='utf-8')
    f3=open("corpus/stat-Slide_Error.log","a",encoding='utf-8')

    f1.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    f2.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    f3.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    global f1,f2,f3
    rating(raw_infilename,std_infilename)
    f1.close()
    f2.close()
    f3.close()

def rating_a_passage_fmm(i):
    raw_infilename='corpus/'+str(i)+'-fmm.txt'
    std_infilename='corpus/'+str(i)+'-std.txt'

    f1=open("corpus/fmm-Concat_Error.log","a",encoding='utf-8')
    f2=open("corpus/fmm-Split_Error.log","a",encoding='utf-8')
    f3=open("corpus/fmm-Slide_Error.log","a",encoding='utf-8')

    f1.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    f2.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    f3.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    global f1,f2,f3
    rating(raw_infilename,std_infilename)

    f1.close()
    f2.close()
    f3.close()

def rating_a_passage_dp_opt(i):
    raw_infilename='corpus/'+str(i)+'-dp_opt.txt'
    std_infilename='corpus/'+str(i)+'-std.txt'

    f1=open("corpus/dp_opt-Concat_Error.log","a",encoding='utf-8')
    f2=open("corpus/dp_opt-Split_Error.log","a",encoding='utf-8')
    f3=open("corpus/dp_opt-Slide_Error.log","a",encoding='utf-8')

    f1.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    f2.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    f3.write('\n\n'+date_str+'\n'+raw_infilename+'\n')
    global f1,f2,f3
    rating(raw_infilename,std_infilename)

    f1.close()
    f2.close()
    f3.close()
    f4.write('\n')

def main():

    start=int(input("start:"))
    stop=int(input("stop:"))
    for i in range(start,stop+1):
        rating_a_passage_fmm(i)
        rating_a_passage_dp_opt(i)
def getdate():
    import time
    date_str=time.asctime()
    date_str=date_str[4:10]+date_str[-5:]
    return date_str
date_str=getdate()
f4=open('corpus/score-'+date_str+'.txt','a',encoding='utf-8')
main()
f4.close()