import re
import string
import scoresys
# -*- coding: utf-8 -*-

def token(sentence_list,dic):

    def not_chinese(p):
        '''p is not chinese iff it is not (1)Letter(2)Number(3)Punc'''
        import dictionary as d
        flag=False
        for tag in d.special_tags.keys():
            if p[0] in d.special_tags[tag]:
                    flag=True
        return flag

    #calcu max_word_len
    max_word_len=0
    for ele in dic:
        if len(ele['Word'])>max_word_len: max_word_len=len(ele['Word'])

    count_times=0
    count_words=len(dic)
    for ele in dic: count_times+=ele['Num']
    average_num=count_times/count_words # Ci2 Pin2
    length_coefficent=[None,2,10,5,16,32,64,128,256,512,1024,2048]#this is parameters
    print('cipin:',average_num)

    def token_sentence(sentence,dic):
        def word_score(phrase,start,stop,dic):
            for ele in dic:
                if phrase[start:stop+1]==ele['Word']:return (ele['Num']+5)*(2**(stop-start+1)-1)
            return 1;

        result_sentence=[]
        for phrase in sentence:
            if len(phrase)<=1:result_sentence.append(phrase)
            elif re.match('[0-9a-zA-Z]+',phrase):result_sentence.append(phrase)
            else:#init
                char_number=len(phrase)
                    #Set the longest word length
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
                phrase_list=phrase.split('|')
                for p in phrase_list:
                    result_sentence.append(p)
                #End for DP
        return result_sentence


        #Now optimize the result


    def correct_concat(result_sentence):
        print("Now correcting concat error!")
        result_word_list=result_sentence.split('|')
        result_word_list.append(None)
        result_word_list.insert(0,None)

        for index in range(1,len(result_word_list)-3):
            if index==1: l_index=0
            else:l_index=index-2

            if index==len(result_word_list)-3:r_index=len(result_word_list)-1
            else:r_index=index+3

            score_std=scoresys.score_after_segment(result_word_list[l_index:r_index],dic)
            score_try=scoresys.score_after_segment(result_word_list[l_index:index]+[result_word_list[index]+result_word_list[index+1]]+result_word_list[index+2:r_index],dic)
            print(result_word_list[l_index:r_index],score_std,
            result_word_list[l_index:index]+[result_word_list[index]+result_word_list[index+1]]+result_word_list[index+2:r_index],
            score_try)

            if score_try>score_std:
                result_word_list[index]=result_word_list[index]+result_word_list[index+1]
                result_word_list.pop(index+1)
                index-=1

        return result_word_list


#        print()




    token_list=[]
    for sentence in sentence_list:
        token_sentence_list=token_sentence(sentence,dic)
        temp_list='|'.join(token_sentence_list)
        token_sentence_list=correct_concat(temp_list)
        for phrase in token_sentence_list:
            token_list.append(phrase)

    return token_list

def stat_seg(text,dic):
    import ss.initialize as init
    '''a method based on stat'''


    import sys
    savedStdout = sys.stdout #娣囨繂鐡ㄩ弽鍥у櫙鏉堟挸鍤ù?
    file=open('log_for_stat_opt.txt', 'w')
    sys.stdout = file #閺嶅洤鍣潏鎾冲毉闁插秴鐣鹃崥鎴ｅ殾閺傚洣娆?
    print('Test for re-direct')

    sentence_list=init.init(text)
##    print(sentence_list)
    token_list=token(sentence_list,dic)
    print(token_list)

    sys.stdout = savedStdout #閹垹顦查弽鍥у櫙鏉堟挸鍤ù?

    return '|'.join(token_list)
