import csv
from re import findall

Virgintime=['Virgin Islands','Puerto Rico']
Easterntime=['Bahamas','ME','NH','MA','VT','RI','CT','NJ','PA','DE','DC','MD','VA','WV','OH','MI','IN','NC','SC','GA','FL','NY']
Mountaintime=['MT','WY','CO','NM','ID','UT','AZ']
Pacifictime=['WA','OR','CA','NV']
Centraltime=['ND','SD','MN','WI','IA','NE','KS','MO','IL','KY','TN','AL','AR','MS','LA','OK','TX']
Hawaiitime=['HI']
Altime=['AK']

for i in range(2000,2014):
    a=str(i)
    year=a[2:]
    fin=open('D:\\Teamstadiums\\teams'+year+'.txt','r')
    a=fin.read()
    stadium=findall('([A-Za-z .&\-\'\(\)]+)\t([0-9\-]+)\t(.+) \((.+), (.+)\)',a)
    stadiumnone=findall('([A-Za-z .&\-\']+)\t([0-9\-]+)\t([noe]+)',a)
    i=0
    data=[]
    #print(stadium[1])
    conferencedict={'-1':'trivial','0':'America East','1':'Atlantic Coast','2':'Atlantic Sun','3':'Atlantic 10','4':'Big East','5':'Big Sky','6':'Big South','7':'Big Ten','8':'Big 12','9':'Big West','10':'Colonial Athletic','11':'Conference USA','12':'Horizon League','13':'Independent','14':'Ivy League','15':'Metro Atlantic Athletic','16':'Mid-American','17':'Mid-Continent','18':'Mid-Eastern','19':'Missouri Valley','20':'Mountain West','21':'Northeast','22':'Ohio Valley','23':'Pacific-12','24':'Patriot League','25':'Southeastern','26':'Southern','27':'Southland','28':'Southwestern Athletic','29':'Sun Belt','30':'West Coast','31':'Western Athletic','32':'Summit','33':'Great West'}
    for item in stadium:
        singleentry=[item[0],item[2],item[3],item[4]]
        if item[1] in conferencedict.keys():
            singleentry.append(conferencedict[item[1]])
        else:
            i=i+1
            singleentry.append('independent'+str(i))
        data.append(singleentry)
    for item in stadiumnone:
        singleentry=[item[0],item[2]]
        if item[1] in conferencedict.keys():
            singleentry.append(conferencedict[item[1]])
            singleentry.append('')
        else:
            i=i+1
            singleentry.append('independent'+str(i))
        data.append(singleentry)
    for item in data:
        try:
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
    fout=open('D:\\Teamstadiums\\teams'+year+'.csv','w',newline='')
    csvWriter=csv.writer(fout,dialect='excel')
    csvWriter.writerows(data)
    fin.close()
    fout.close()
