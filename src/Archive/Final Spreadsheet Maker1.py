import csv

for i in range(2000,2014):
    a=str(i)
    yearshort=a[2:]
    #print(yearshort)
    finmatch=open('D:\\Matchinfo\\Finalspreadsheet'+yearshort+'.csv','r')
    csvReader=csv.reader(finmatch)
    data=[]
    index=0
    for item in csvReader:
        index=index+1
        singleentry=[]
        if index==1:
            singleentry=singleentry+item[0:2]
            singleentry.append(item[10])
            singleentry.append(item[9])
            singleentry.append(item[18])
            singleentry.append(item[24])
            singleentry=singleentry+['1st Half Score Differential','2nd Half Score Differential','OT Score Differential']+item[6:8]+item[15:17]
            singleentry.append(item[22])
            singleentry.append(item[8])
            singleentry.append(item[17])
            singleentry=singleentry+item[25:]
        else:
            temp1=int(item[11])-int(item[2])
            temp2=int(item[12])-int(item[3])
            temp3=int(item[13])-int(item[4])
            singleentry=singleentry+item[0:2]
            singleentry.append(item[10])
            singleentry.append(item[9])
            singleentry.append(item[18])
            singleentry.append(item[24])
            singleentry=singleentry+[str(temp1),str(temp2),str(temp3)]+item[6:8]+item[15:17]
            singleentry.append(item[22])
            singleentry.append(item[8])
            singleentry.append(item[17])
            singleentry=singleentry+item[25:]
        #singleentry=singleentry+item[0:2]+item[10]+item[9]+item[18]+item[24]+[]+item[6:8]+item[15:18]+item[22]+item[8]+item[17]+item[25:]
        data.append(singleentry)
    finmatch.close()
    foutmatch=open('D:\\Matchinfo\\Finalspreadsheetadjusted'+yearshort+'.csv','w',newline='')
    csvWriter=csv.writer(foutmatch,dialect='excel')
    csvWriter.writerows(data)
    foutmatch.close()
    
