import csv

for i in range(2000,2014):
    s='D:\\Matchinfo\\'+str(i)+'with courtinfo.csv'
    fin=open(s,'r')
    csvReader=csv.reader(fin)
    data=[]
    for item in csvReader:
        try:
            if (item[12]=='Lexington')and(item[13]=='KY'):
                item[14]=0
            if (item[12]=='Louisville')and(item[13]=='KY'):
                item[14]=0
            if (item[12]=='Morehead')and(item[13]=='KY'):
                item[14]=0
            if (item[12]=='Richmond')and(item[13]=='KY'):
                item[14]=0
            if (item[12]=='Chattanooga')and(item[13]=='TN'):
                item[14]=0
            if (item[12]=='Johnson City')and(item[13]=='TN'):
                item[14]=0
            if (item[12]=='Knoxville')and(item[13]=='TN'):
                item[14]=0
            if (item[12]=='Evansville')and(item[13]=='IN'):
                item[14]=1
            if (item[12]=='Oakland City')and(item[13]=='IN'):
                item[14]=1
            if (item[12]=='Valparaiso')and(item[13]=='IN'):
                item[14]=1
            if (item[12]=='Moscow')and(item[13]=='ID'):
                item[14]=3
            data.append(item)
        except:
            pass
    fin.close()
    year=str(i)
    s1='D:\\Teamstadiums\\teams'+year[2:]+'.csv'
    fin=open(s1,'r')
    csvReader=csv.reader(fin)
    teamdict={}
    for itemm in csvReader:
        teamdict[itemm[0]]=itemm[4]
    #print(teamdict)
    #print(data[1])
    for item in data[1:]:
        try:
            if item[1] in teamdict.keys():
                ATtzdifference=str(abs(int(teamdict[item[1]])-int(item[14])))
            else:
                ATtzdifference='-1'
            if item[6] in teamdict.keys():
                HTtzdifference=str(abs(int(teamdict[item[6]])-int(item[14])))
            else:
                HTtzdifference='-1'
            item.append(ATtzdifference)
            item.append(HTtzdifference)
            #print(item)
        except:
            pass
    fin.close()
    data[0].append('AT Timezone Difference')
    data[0].append('HT Timezone Difference')
    fout=open(s,'w',newline='')
    csvWriter=csv.writer(fout,dialect='excel')
    csvWriter.writerows(data)
    fout.close()
