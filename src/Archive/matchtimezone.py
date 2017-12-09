import csv

for i in range(2000,2013):
    a='D:\\Matchinfo\\'+str(i)+'courtinfo.csv'
    fin=open(a,'r')
    csvReader=csv.reader(fin)
    data=[]
    Virgintime=['Virgin Islands','Puerto Rico']
    Easterntime=['Bahamas','ME','NH','MA','VT','RI','CT','NJ','PA','DE','DC','MD','VA','WV','OH','MI','IN','NC','SC','GA','FL','NY']
    Mountaintime=['MT','WY','CO','NM','ID','UT','AZ']
    Pacifictime=['WA','OR','CA','NV']
    Centraltime=['ND','SD','MN','WI','IA','NE','KS','MO','IL','KY','TN','AL','AR','MS','LA','OK','TX']
    Hawaiitime=['HI']
    Altime=['AK']
    data=[]
    for item in csvReader:
        if item[1] in Easterntime:
            item=item[0:2]+['0']
        elif item[1] in Centraltime:
            item=item[0:2]+['1']
        elif item[1] in Mountaintime:
            item=item[0:2]+['2']
        elif item[1] in Pacifictime:
            item=item[0:2]+['3']
        elif item[1] in Hawaiitime:
            item=item[0:2]+['5']
        elif item[1] in Altime:
            item=item[0:2]+['4']
        elif item[1] in Virgintime:
            item=item[0:2]+['-1']
        else:
            item=item[0:2]+['']
        data.append(item)
    fin.close()
    fout=open(a,'w',newline='')
    csvWriter=csv.writer(fout)
    csvWriter.writerows(data)
    fout.close()
    
