import dictionary as d
def score_after_segment(origin_list,dic):
    '''get a word_list and a dic, return a score'''
    max_word_len=0
    for ele in dic:
        if len(ele['Word'])>max_word_len: max_word_len=len(ele['Word'])

    count_times=0
    count_words=len(dic)
    for ele in dic: count_times+=ele['Num']
    average_num=count_times/count_words # Ci2 Pin2
    length_coefficent=[None,2,10*2,10*3,16*4,32*5,64*6,128*7,256*8,512*9,1024*10,2048*11]#this is parameters
#    print('cipin:',average_num)



    def not_chinese(p):
        '''p is not chinese iff it is not (1)Letter(2)Number(3)Punc'''
        import dictionary as d
        flag=False
        for tag in d.special_tags.keys():
            if p[0] in d.special_tags[tag]:
                    flag=True
        return flag

    import math
    std_score=0
    phrase_list=origin_list[:]
    phrase_list.insert(0,None)
    phrase_list.append(None)

    for index in range(len(phrase_list)):
        phrase=phrase_list[index]
#        print('in_s_a_s:phrase',phrase)
        if phrase==None: continue
        if phrase=='':continue

        flag=False
        for tag in d.special_tags.keys():
            if phrase[0] in d.special_tags[tag]:
                flag=True
        if flag:continue

        in_dic=False

        for ele in dic:
            if phrase == ele['Word']:
                in_dic=True
                std_score+=length_coefficent[len(phrase)]
                prefix_match=ele['Pre'].get(phrase_list[index-1],1)
                suffix_match=ele['Suf'].get(phrase_list[index+1],1)
                average_match=(prefix_match+suffix_match)/2
                #Max?Min?Ave?
#                print(prefix_match,suffix_match,average_num)
                ratio=float(average_match)/float(average_num)
                std_score+=math.log10(ratio*10)*10
#                print(phrase,math.log10(ratio*10)*10)
##                if (ratio>=1):std_score+=math.log10(ratio*10)*10
##                if (ratio<1):std_score+=math.sqrt(ratio)*10-10
                #The scoring method#

                break
        if (in_dic==False):std_score-=5 # this is a parameter

    return std_score

if __name__=='__main__':
#for test
    dic,u=d.getdict()
    text='''工作组|织|上|的|贸易|错|开|发票|等'''
    t_l=text.split('|')
    print(t_l,score_after_segment(t_l,dic))
