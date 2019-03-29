import re
import string
punctuation=string.punctuation
chnpunctuation='，。、？！……：；“‘”’{}【】《》——（）'
pausepunctuation='，。、？！……：；'
special_tags={'NUMBER':'0123456789','PUNC':chnpunctuation+string.punctuation,'LETTER':''}
for i in range(26):special_tags['LETTER']+=chr(ord('a')+i);
for i in range(26):special_tags['LETTER']+=chr(ord('A')+i);

def not_chinese(p):
    '''p is not chinese iff it is not (1)Letter(2)Number(3)Punc'''
    flag=False
    for tag in special_tags.keys():
        if p[0] in special_tags[tag]:
                flag=True
    return flag

def token_sentence(text):
    '''return a list, each element is a sentence'''
    text=re.sub(r'([，。？！：；])',r'|\1|',text)
    text=re.sub(r'[　 \t\n]+','|',text)
    if '||' in text: text=text.replace('||','|')
    sentence_list=text.split('|')
    
    if ('\n' in sentence_list):sentence_list.remove('\n')
    if ('' in sentence_list):sentence_list.remove('')
    return sentence_list

def remove_num_and_punc(sentence):

    #remove english punc
    for char in string.punctuation:
        if char in sentence: sentence=sentence.replace(char,'|'+char+'|')
    #remove chinese punc and letter and numeric
    word_str=re.sub(r'([0-9a-zA-Z]+|[“‘”’{}、【】《》——（）])',r'|\1|',sentence)
    word_list=word_str.split('|')
    while ('' in word_list): word_list.remove('')
    return(word_list)
            
def init(text):
    '''return a list, each element is a list of words(with tokened num and punc)'''
    sentence_list=token_sentence(text)
    for i in range(len(sentence_list)):
        sentence_list[i]=remove_num_and_punc(sentence_list[i])
    return sentence_list
    
