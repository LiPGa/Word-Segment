import string
punctuation=string.punctuation
chnpunctuation='，。、？！……：；“‘”’{}【】《》——（）'
pausepunctuation='，。、？！……：；'
special_tags={'NUMBER':'0123456789','PUNC':chnpunctuation+string.punctuation,'LETTER':''}
for i in range(26):special_tags['LETTER']+=chr(ord('a')+i);
for i in range(26):special_tags['LETTER']+=chr(ord('A')+i);

def getdict():
        '''return a tuple(dic, url_list)'''
        def getline(line):
                w={}
                #{'Word': ,'Num': ,'Pre':[dict] , 'Suf':[dict] }

                def list_word(line):
                        fix={}
                        list=line.split(',')
                        for ele in list:
                                pair=ele.split(':')
                                fix[pair[0]]=int(pair[1])
                        return fix

                index=line.find('|Word|')
                w['Word']=line[:index]
                line=line[index+len('|Word|'): ]

                index=line.find('|Num|')
                w['Num']=int(line[:index])
                line=line[index+len('|Num|'): ]

                index=line.find(',|Pre|')
                w['Pre']=list_word(line[:index])
                line=line[index+len(',|Pre|'): ]

                index=line.find(',|Suf|')
                w['Suf']=list_word(line[:index])
                line=line[index+len(',|Suf|'): ]

                return w
        
        ver_file=open('dict/latest.log','r',encoding='UTF-8')      
        ver=ver_file.readline()
        ver=ver.replace('\n','')

        url_list=[]
        url_file=open('dict/'+ver[:-3]+'log','r',encoding='UTF-8')
        while True:
                line=url_file.readline()
                if (line==''):break;
                url_list.append(line)
                
        dic_file=open('dict/'+ver,'r',encoding='UTF-8')
        dic=[]
        while True:
                line=dic_file.readline()
                if (line==''): break
                flag=True
                for tag in special_tags.keys():
                    if line[0] in special_tags[tag]:flag=False
                if flag: dic.append(getline(line))
        return dic,url_list


def train_one_passage(dic,url_list,text_str):
        def splitwords(text):
                text=text.replace('｜','|')
                if(text[0]!='|'):text='|'+text
                if(text[-1]!='|'):text=text+'|'
                text_list=list(text)

                char_list=[]
                for i in range(len(text_list)):
                        char=text_list[i]
                        if ((char in punctuation)and not(char=='|')):char_list.append('|'+char+'|')
                        elif ((char=='\n')or(char=='　')or(char==' ')or(char=='\t')):pass
                        elif (char in pausepunctuation):char_list.append('|'+char+'|')
                        elif (char in chnpunctuation):char_list.append('|'+char+'|')
                        else:char_list.append(char)
                text=''.join(char_list)
                while ('||' in text):text=text.replace('||','|')
                        
                #Remove punctuation

                
                word_seq=text.split('|')
                if word_seq[0]=='': word_seq=word_seq[1:]
                if word_seq[-1]=='': word_seq=word_seq[:-1]
                word_num=len(word_seq)-2
                #Add special tags
                for index in range(len(word_seq)):
                        for tag in special_tags.keys():
                                if word_seq[index][0] in special_tags[tag]:
                                        word_seq[index]=tag
                                        break
                #Tag the beginning or end of sentence 
                word_seq[0],word_seq[-1]='None','None'

                return(word_seq)
                
        def add_to_dict(dic,word_seq):
                def search(word,dic):
                        for i in range(len(dic)):
                                if (dic[i]['Word']==word):return i

                        return -1

                def insert(fix,word):
                        #dic is {'的': 1},{'是':1}
                        fix[word]=fix.get(word,0)+1
                        return fix

                #{'Word': ,'Num': ,'Pre':[dict] , 'Suf':[dict] }
                
                for i in range(len(word_seq)):
                        if (word_seq[i]=='None') : continue
                        index=search(word_seq[i],dic)
                        if (index>=0):
                                temp=dic[index]
                                temp['Num']+=1
                                temp['Pre']=insert(temp['Pre'],word_seq[i-1])
                                temp['Suf']=insert(temp['Suf'],word_seq[i+1])
                                dic[index]=temp
                        else:
                                d={}
                                d['Word']=word_seq[i]
                                d['Num']=1
                                d['Pre']={word_seq[i-1]:1}
                                d['Suf']={word_seq[i+1]:1}
                                dic.append(d)
                dic=sorted(dic,key=lambda dic:dic['Num'])

        #check if the url appears in list
        
        f=open(text_str,'r',encoding='UTF-8')
        url=f.readline()
        while not(str.isalpha(url[0])):url=url[1:]
        
        if (url in url_list):
                print('Warning:This article has been trained before')
                return
        url_list.append(url)
        
        text=f.read()
        word_seq=splitwords(text)
        add_to_dict(dic,word_seq)


def output_to_dict(dic,url_list):
        def getdate():
                import time
                date_str=time.asctime()
                date_str=date_str[4:10]+date_str[-5:]
                return date_str

        def freshdict(dic,file_str):
                '''This output dic into a .dic file'''
                def format_fix(fix_dict):# for Prefix and Suffix
                        ret=''
                        for ele in fix_dict.keys():
                                ret=ret+ele+':'+str(fix_dict[ele])+','
                        return ret
                f=open(file_str,'w',encoding='UTF-8')
                for entry in dic:
                        f.write("{0}|Word|{1}|Num|{2}|Pre|{3}|Suf|\n"
                                .format(entry['Word'],entry['Num'],format_fix(entry['Pre']),format_fix(entry['Suf'])))
                f.close()

        def freshurl(url_list,file_str):
                """This output new_url_list into a .log file"""
                f=open(file_str,'w',encoding='UTF-8')
                for ele in url_list:
                        f.write(ele)
                f.close()
        
        #Refresh Version Information
        f=open("dict/latest.log","w")
        date_str=getdate()
        file_str=date_str+'.dic'
        f.write(file_str+'\n')
        f.close()
        freshdict(dic,"dict/"+file_str)

        file_str=date_str+'.log'
        freshurl(url_list,"dict/"+file_str)

