import csv

fname='D:\\Matchinfo\\Finalspreadsheet13adjusted.csv'
fin=open(fname,'r')
csvReader=csv.reader(fin)

coefficientdict={}
for i1 in range(1,4):
    firstdig=1.25-0.25*i1
    for i2 in range(4,8):
        seconddig=7/3-1/3*i2
        if i2==7:
            ii2=0
        else:
            ii2=i2
        for i3 in range(7,11):
            if i3<10:
                thirddig=9.7/3-1/3*i3
                ii3=i3
            else:
                thirddig=0
                ii3=0
            coefficientdict[str(i1*100+ii2*10+ii3)]=round(firstdig*(seconddig-thirddig),4)
index=0
total=[]
for item in csvReader:
    if index==0:
        title=item[37:63]
        total.append(item)
        coefficientdict1=coefficientdict.copy()
        for item1 in coefficientdict.keys():
            if item1 in title:
                pass
            else:
                coefficientdict1.pop(item1, None)
        coefficientdict=coefficientdict1
        coefficientdictcol={}
        for index1 in range(37,63):
            coefficientdictcol[index1]=item[index1]
        print(coefficientdictcol)
        index=index+1
    else:
        for index1 in range(37,63):
            if item[index1]=='1':
                item[63]=coefficientdict[coefficientdictcol[index1]]
        total.append(item)
        index=index+1

fin.close()
fout=open(fname,'w',newline='')
csvWriter=csv.writer(fout)
csvWriter.writerows(total)
fout.close()
