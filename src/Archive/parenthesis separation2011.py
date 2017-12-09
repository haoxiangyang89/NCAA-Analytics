import csv
from re import findall

fin=open('D:\\Matchinfo\\2012.csv','r')
csvReader=csv.reader(fin)
data=[]
courtinfo=[]
for item in csvReader:
    #print(item)
    try:
        data.append(item[11])
    except:
        courtinfo.append(['',''])
i=0
for item in data:
    try:
        if i!=0:
            a=findall('\((.+)\)',item)
            #print(a)
            b=a[0].split(',')
            b[1]=b[1].strip()
            courtinfo.append(b)
            #print(b)
        i=i+1
    except:
        courtinfo.append(['',''])
fout=open('D:\\Matchinfo\\2012courtinfo.csv','w',newline='')
csvWriter=csv.writer(fout)
csvWriter.writerows(courtinfo)

fout.close()
fin.close()
