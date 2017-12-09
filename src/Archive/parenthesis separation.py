import csv
from re import findall

fin=open('D:\\1\\2001.csv','r')
csvReader=csv.reader(fin)
data=[]
for item in csvReader:
    print(item)
    data.append(item[11])
i=0
courtinfo=[]
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
fout=open('D:\\1\\2001courtinfo.csv','w',newline='')
csvWriter=csv.writer(fout)
csvWriter.writerows(courtinfo)

fout.close()
fin.close()
