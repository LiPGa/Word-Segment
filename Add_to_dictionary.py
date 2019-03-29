import dictionary as d

def main():
    start=int(input("start:"))
    stop=int(input("stop:"))

    for i in range(start,stop+1):
        dic,url_list=d.getdict()
        d.train_one_passage(dic,url_list,text_str='corpus/'+repr(i)+'-std.txt')
        d.output_to_dict(dic,url_list)


main()
