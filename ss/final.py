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





    def correct_concat(origin_sentence_text):
        print("\n\nNow correcting concat error!")
        origin_sentence_list=origin_sentence_text.split('|')

        if ('' in origin_sentence_list):origin_sentence_list.remove('')
        result_word_list=origin_sentence_text.split('|')
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
##                print(increment)
                print(newword)
                if newword in word_list:
                    print('Newword',newword,'in dic')
                    score_std=scoresys.score_after_segment(result_word_list[index-1:right_index+2],dic)
                    score_try=scoresys.score_after_segment([result_word_list[index-1]]+[newword]+[result_word_list[right_index+1]],dic)
                    print(score_std,result_word_list[index-1:right_index+2],score_try,[result_word_list[index-1]]+[newword]+[result_word_list[right_index+1]])

                    if score_try>score_std:
                        result_word_list=result_word_list[:index]+[newword]+result_word_list[right_index+1:]
                        origin_sentence_list=origin_sentence_list[:index]+[newword]+origin_sentence_list[right_index+1:]

##            print(result_word_list)

  ##      print(origin_sentence_list[1:-1])
        return origin_sentence_list[1:-1]

    def correct_slide(origin_sentence_list):
        print('Now correcting slide error')
        def try_slide(word_list,index):

            if not_chinese(word_list[index]):return word_list
            if not_chinese(word_list[index+1]):return word_list

            if len(try_sentence_list[index])>1:#AB|C to A|BC
                word_list_before=word_list[index-1:index+3]
                #pre|AB|C|suf

                word_list_after=word_list_before[:]
                word_list_after[2]=word_list_after[1][-1]+word_list_after[2][:]
                word_list_after[1]=word_list_after[1][:-1]
##                print('AB|C to A|BC',word_list_before,word_list_after)
                #pre|A|BC|suf
                score_std=scoresys.score_after_segment(word_list_before,dic)
                score_try=scoresys.score_after_segment(word_list_after,dic)

                print('Congratulation:',word_list_before,'to',word_list_after)
                if score_std<score_try: word_list[index-1:index+3]=word_list_after

            if len(try_sentence_list[index+1])>1:#A|BC to AB|C
                word_list_before=word_list[index-1:index+3]
                #pre|A|BC|suf

                word_list_after=word_list_before[:]
                word_list_after[1]=word_list_after[1][:]+word_list_after[2][0]
                word_list_after[2]=word_list_after[2][1:]

##                print('A|BC to AB|C',word_list_before,word_list_after)
                #pre|AB|C|suf
                score_std=scoresys.score_after_segment(word_list_before,dic)
                score_try=scoresys.score_after_segment(word_list_after,dic)

                if score_std<score_try:

                    print('Congratulation:',word_list_before,'to',word_list_after)
                    word_list[index-1:index+3]=word_list_after
            return word_list

        try_sentence_list=origin_sentence_list[:]

##        print(try_sentence_list)
        import dictionary as d
        for index in range(len(origin_sentence_list)):
            for tag in d.special_tags.keys():
                if try_sentence_list[index]=='':break
                if try_sentence_list[index][0] in d.special_tags[tag]:
                    try_sentence_list[index]=tag
                    break


        try_sentence_list.append(None)
        try_sentence_list.insert(0,None)


##        print(try_sentence_list)
        for index in range(1,len(try_sentence_list)-3):
##            print(index)
            try_sentence_list=try_slide(try_sentence_list,index)

        try_sentence_list=try_sentence_list[1:-1]
        for index in range(len(origin_sentence_list)):
            if not_chinese(try_sentence_list[index]):try_sentence_list[index]=origin_sentence_list[index]

        return try_sentence_list



    token_list=[]
    for sentence in sentence_list:
        token_sentence_list=token_sentence(sentence,dic)

        token_sentence_list=correct_slide(token_sentence_list)

        token_sentence_list=correct_concat('|'.join(token_sentence_list))

        for phrase in token_sentence_list:
            token_list.append(phrase)
#    print(token_list)
    return token_list


def segment(text,dic):
    import ss.initialize as init
    '''a method based on stat'''


    import sys
    savedStdout = sys.stdout #婵烇絽娲︾换鍌炴偤閵娾晛鍐€闁搞儜鍐╃彲闁哄鐗婇幐鎼佸吹椤撶伝?
    file=open('log_for_final.txt', 'w')
    sys.stdout = file #闂佸搫绉村ú銈夊闯椤栨稒缍囬柟鎯у暱濮ｅ姊洪幓鎺斝㈤柣锝夌畺瀹曘儵骞嬮敐鍛啎闂佸搫鍊稿ú锝呪枎?
    print('Test for re-direct')

    sentence_list=init.init(text)
    print(sentence_list)
    token_list=token(sentence_list,dic)
    print(token_list)

    sys.stdout = savedStdout #闂佽鍘归崹褰捤囬弻銉ュ唨闁搞儜鍐╃彲闁哄鐗婇幐鎼佸吹椤撶伝?

    return '|'.join(token_list)

