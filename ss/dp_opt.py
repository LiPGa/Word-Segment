import re
import string
import scoresys

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
    word_list=[]
    #Pre calcu
    max_word_len=0
    for ele in dic:
        word_list.append(ele['Word'])
        if len(ele['Word'])>max_word_len: max_word_len=len(ele['Word'])

  ##  print(max_word_len,' is length longest')
    count_times=0
    count_words=len(dic)
    for ele in dic: count_times+=ele['Num']
    average_num=count_times/count_words # Ci2 Pin2
    length_coefficent=[None,2,10,5,16,32,64,128,256,512,1024,2048]#this is parameters
#    print('cipin:',average_num)
    #Pre calcu end//

    def token_sentence(sentence,dic):
        def word_score(phrase,start,stop,dic):
            for ele in dic:
                if phrase[start:stop+1]==ele['Word']:return (ele['Num']+5)*(3**(stop-start+1)-1)
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
                for i in range(char_number+max_word_len):
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
        return result_sentence





    def correct_concat(origin_sentence):
#        print("\n\nNow correcting concat error!")
        origin_sentence_list=origin_sentence.split('|')

        if ('' in origin_sentence_list):origin_sentence_list.remove('')
        result_word_list=origin_sentence.split('|')
        if ('' in result_word_list):result_word_list.remove('')
#        print(result_word_list)


        import dictionary as d
        for index in range(len(result_word_list)):
            for tag in d.special_tags.keys():
                if result_word_list[index]=='':break
                if result_word_list[index][0] in d.special_tags[tag]:
                    result_word_list[index]=tag
                    break
        result_word_list.append(None)
        result_word_list.insert(0,None)

        origin_sentence_list.append(None)
        origin_sentence_list.insert(0,None)

#        print(result_word_list)
#        print(origin_sentence_list)

        index=0
        while index<len(result_word_list)-2:
            index+=1
     ##       print(index)
            if result_word_list[index]==None:continue
            if result_word_list[index][0] in string.ascii_uppercase:continue #Not Chinese

            #Now Try to create new words

            for increment in range(max_word_len,0,-1):
                flag=True
                newword=result_word_list[index]
                for right_index in range(index+1,index+increment+1):
                    if result_word_list[right_index]==None:
                        flag=False
                        break
                    if result_word_list[right_index][0] in string.ascii_uppercase:
                        flag=False
                        break
                    newword=newword+result_word_list[right_index]

                if flag==False:continue
    ##            print(increment)
   ##             print(newword)
                if newword in word_list:
   ##                 print('Newword',newword,'in dic')
                    score_std=scoresys.score_after_segment(result_word_list[index-1:right_index+2],dic)
                    score_try=scoresys.score_after_segment([result_word_list[index-1]]+[newword]+[result_word_list[right_index+1]],dic)
  ##                  print(score_std,result_word_list[index-1:right_index+2],score_try,[result_word_list[index-1]]+[newword]+[result_word_list[right_index+1]])

                    if score_try>score_std:
                        result_word_list=result_word_list[:index]+[newword]+result_word_list[right_index+1:]
                        origin_sentence_list=origin_sentence_list[:index]+[newword]+origin_sentence_list[right_index+1:]

##            print(result_word_list)

  ##      print(origin_sentence_list[1:-1])
        return origin_sentence_list[1:-1]




    token_list=[]
    for sentence in sentence_list:
        token_sentence_list=token_sentence(sentence,dic)

        token_sentence_list=correct_concat('|'.join(token_sentence_list))

        for phrase in token_sentence_list:
            token_list.append(phrase)
#    print(token_list)
    return token_list


def segment(text,dic):
    import ss.initialize as init
    '''a method based on stat'''


##    import sys
##    savedStdout = sys.stdout #娣囨繂鐡ㄩ弽鍥у櫙鏉堟挸鍤ù?
##    file=open('log_for_stat_opt.txt', 'w')
##    sys.stdout = file #閺嶅洤鍣潏鎾冲毉闁插秴鐣鹃崥鎴ｅ殾閺傚洣娆?
##    print('Test for re-direct')

    sentence_list=init.init(text)
#    print(sentence_list)
    token_list=token(sentence_list,dic)
##    print(token_list)

##    sys.stdout = savedStdout #閹垹顦查弽鍥у櫙鏉堟挸鍤ù?

    return '|'.join(token_list)

