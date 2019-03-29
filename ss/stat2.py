import re
# -*- coding: utf-8 -*-
def word_score(phrase,start,stop,dic):
    for ele in dic:
        if phrase[start:stop+1]==ele['Word']:return (ele['Num']+5)*(2**(stop-start+1)-1)
    return 1;

def token(sentence,dic):
    result_sentence=[]
    for phrase in sentence:
        if len(phrase)<=1:result_sentence.append(phrase)
        elif re.match('[0-9a-zA-Z]+',phrase):result_sentence.append(phrase)
        else:#init
            char_number=len(phrase)
            max_word_len=5#Set the longest word length
            score=[]
            index=[]# records index of the first char of this word
            for i in range(char_number+5):
                index.append(0)
                score.append(0)
            #init//
            #DP
            for i in range(char_number):#i is the presenting index
                max_score=0
                max_score_j=0#max_match_j records index of the first char of this word
                for j in range(1,max_word_len+1):#search for length
                    now_score=0
                    if (i-j+1)<0:continue
                    if (i-j+1)==0:
                        now_score=word_score(phrase,i-j+1,i,dic)
                        if now_score>max_score:
                            max_score=now_score
                            max_score_j=i-j+1
                    if (i-j+1)>0:
                        now_score=word_score(phrase,i-j+1,i,dic)+score[i-j]
                        if now_score>max_score:
                            max_score=now_score
                            max_score_j=i-j+1

                score[i]=max_score
                index[i]=max_score_j
            i = char_number-1
            while (i>=0):
                phrase=phrase[0:index[i]]+'|'+phrase[index[i]:]
                i=index[i]-1
            if (phrase[0]=='|'):phrase=phrase[1:]
            result_sentence.append(phrase)
    return result_sentence




def stat_seg(text,dic):
    import ss.initialize as init
    '''a method based on stat'''
    sentence_list=init.init(text)
    token_list=[]
    for sentence in sentence_list:
        token_sentence_list=token(sentence,dic)
        for phrase in token_sentence_list:
            token_list.append(phrase)
    return '|'.join(token_list)
#测试中文编码
