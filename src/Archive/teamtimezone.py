import csv

year=['00','01','02','03','04','05','06','07','08','09','10','11','12','13']

for i in year:
    a='D:\\Teamstadiums\\teams'+i+'.csv'
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
        if item[3] in Easterntime:
            item.append('0')
        elif item[3] in Centraltime:
            item.append('1')
        elif item[3] in Mountaintime:
            item.append('2')
        elif item[3] in Pacifictime:
            item.append('3')
        elif item[3] in Hawaiitime:
            item.append('5')
        elif item[3] in Altime:
            item.append('4')
        elif item[3] in Virgintime:
            item.append('-1')
        else:
            item.append('')
        try:
            if (item[2]=='Lexington')and(item[3]=='KY'):
                item[5]='0'
            if (item[2]=='Louisville')and(item[3]=='KY'):
                item[5]='0'
            if (item[2]=='Morehead')and(item[3]=='KY'):
                item[5]='0'
            if (item[2]=='Richmond')and(item[3]=='KY'):
                item[5]='0'
            if (item[2]=='Chattanooga')and(item[3]=='TN'):
                item[5]='0'
            if (item[2]=='Johnson City')and(item[3]=='TN'):
                item[5]='0'
            if (item[2]=='Knoxville')and(item[3]=='TN'):
                item[5]='0'
            if (item[2]=='Evansville')and(item[3]=='IN'):
                item[5]='0'
            if (item[2]=='Oakland City')and(item[3]=='IN'):
                item[5]='1'
            if (item[2]=='Valparaiso')and(item[3]=='IN'):
                item[5]='1'
            if (item[2]=='Moscow')and(item[3]=='ID'):
                item[5]='3'
        except:
            pass
        data.append(item)
    fin.close()
    fout=open(a,'w',newline='')
    csvWriter=csv.writer(fout)
    csvWriter.writerows(data)
    fout.close()
    
