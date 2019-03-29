import tkinter
from tkinter import *
import re
import dictionary
import tkinter.messagebox

root=Tk()
root.title('TrainingUI')

SourcePath=StringVar()
SourceFile=StringVar()
TargetFile=StringVar()
QueryResult=StringVar()
QText=StringVar()

head=Frame(root,borderwidth=10)

sp_text=Entry(head,width=40,textvariable=SourcePath)
sf_text=Entry(head,width=20,textvariable=SourceFile)



qtext=Entry(head,width=20,textvariable=QText)
queryButton=Button(head,text='Query',command=lambda foo=0:Query())
queryLabel=Label(head,textvariable=QueryResult,font=('Helvectica',20))

text_fr=Frame(root,borderwidth=10)
tail=Frame(root,borderwidth=10)

text =Text(bg='white', height=20,font=('Helvectica',26))

global unmodified_flag
unmodified_flag=True
ctrl_flag=False
c_flag=False


def Load():
    global unmodified_flag
    if not(unmodified_flag):
       answer=tkinter.messagebox.askquestion("Save", "Sure To Load? Something modified may be lost.")
       if answer=='no': return

    s=SourcePath.get()+SourceFile.get()
    f=open(s,'r',encoding='UTF-8')
    text.delete(0.0,END)
    text.insert(END,f.read())
    f.close()
    TargetFileName=str(re.findall(r'[0-9]+',s)[0])+'-std.txt'
    TargetFile.set(TargetFileName)
    unmodified_flag=False

def Save():

    global unmodified_flag
    answer=tkinter.messagebox.askquestion("Save", "Sure To Save?")

    if answer=='yes' :
        unmodified_flag=True
        TargetFileStr=SourcePath.get()+TargetFile.get()

        f=open(TargetFileStr,'w',encoding='UTF-8')
        f.write(text.get(0.0,END))
        f.close

        index=int(re.findall(r'[0-9]+',SourceFile.get())[0])
        SourceFileStr=SourceFile.get()
        SourceFileStr=re.sub(r'[0-9]+',repr(index+1),SourceFileStr)

        SourceFile.set(SourceFileStr)
        unmodified_flag=True
def Query():

    dic,url_list=dictionary.getdict()
    word_list=[]
    for ele in dic:
        word_list.append(ele["Word"])

    queryword=queryLabel.clipboard_get()
    q_list=list(queryword)
    while '|' in q_list:q_list.remove('|')
    queryword=''.join(q_list)
    if queryword in word_list:QueryResult.set(queryword+' is IN dictionary')
    else:QueryResult.set(queryword +' is NOT in dictionary')

def check(flag):
    if (flag):Query()

def boolassign(assignstr):
    print(assignstr)
    exec(assignstr)

def reportEvent(event):
    Query()

def main():

    unmodified_flag=True

    tf_text=Entry(tail,width=20,textvariable=TargetFile)

    #<head>
    #<SourcePath>
    label1=Label(head,text="SourcePath")
    label1.pack(side=LEFT,)
    SourcePath.set('corpus/')
    sp_text.pack(side=LEFT,)
    #<SourcePath/> var:SourcePath

    #<SourceFile>
    label2=Label(head,text="SourceFile")
    label2.pack(side=LEFT,)

    start_index=input("Which article to train first('x' or 'x-fmm')")
    SourceFile.set(start_index+'.txt')
    sf_text.pack(side=LEFT)
    #<SourceFile/>var:SourceFile

    #<Button>
    ButtonLoad=Button(head,text='Load',command=lambda foo=0:Load())
    ButtonLoad.pack(side=LEFT)
    head.pack(side=TOP,expand=YES,anchor=NW,fill=X)
    #<Button/>
    ##<head/>

    ##<text_frame>
    #<text>
    text.bind('<Control-q>',reportEvent)
##    text.bind('<Control_R>',reportEvent)
##    text.bind('<C>',reportEvent)
##    text.bind('<KeyPress>',reportEvent)

    text.pack(side=TOP,fill=Y)
    #<text/>
    text_fr.pack(expand=NO)

    QText.set("Here is used to buffer the to-query word")
    qtext.pack(side=LEFT)
    queryButton.pack(side=LEFT,fill=X)
    queryLabel.pack(side=LEFT,fill=X,padx=10)
    ##<text_frame/>

    ##<tail>
    #<TargetFile>
    label_instruct=Label(tail,text="Quick Query:\nCtrl+C to copy the word to the cliperboard\n Then Ctrl+Q to query\n")
    label_instruct.pack(side=TOP,expand=NO,anchor=W)
    label3=Label(tail,text="TargetFile")
    label3.pack(side=LEFT,expand=YES,fill=X)
    TargetFile.set('TargetFile')
    tf_text.pack(side=LEFT,expand=YES,fill=X)
    #<TargetFile/>var:TargetFile
    #<ButtonSave>
    ButtonSave=Button(tail,text='Save',command=lambda foo=0:Save())
    ButtonSave.pack(side=LEFT)
    #<ButtonSave//>
    tail.pack(side=TOP)
    ##<tail>
    ButtonLoad.focus()
    mainloop()
main()
