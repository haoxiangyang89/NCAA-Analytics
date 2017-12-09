# Integrated codes for NCAA data collecting and compiling
# 3/21/2014

import os
import urllib.request
import csv
from re import findall
from tkinter import *
from operator import *
from datetime import *

class NCAAdatacompiler:
    
    def convertDate2(self,datee):
        array=datee.split('/')
        return date(year=int(array[2]),month=int(array[0]),day=int(array[1]))
    
    def inputDate(self):
        startDate=self.startDatestr.get()
        endDate=self.endDatestr.get()
        try:
            self.startDated=self.convertDate2(startDate)
            if endDate!="":
                self.endDated=self.convertDate2(endDate)
            else:
                self.endDated=self.startDated
        except:
            messagebox.showerror("Error","Please input a starting date")
            
    
    def extractDay(self,dated):
        year=str(dated.year)
        month=str(dated.month)
        day=str(dated.day)
        address="http://rivals.yahoo.com/ncaa/basketball/scoreboard?d="+year+"-"+month+"-"+day
        webFile=urllib.request.urlopen(address)
        localFile=open(year+"-"+month+"-"+day+".source.html","wb")
        st=webFile.read()
        localFile.write(st)
        webFile.close()
        localFile.close()
    
    def parenthesissep(self,thisgameinfo):
        st=thisgameinfo[-1]
        if st!='':
            try:
                temp1=findall('\((.+)\)',st)
                temp2=temp1[0].split(',')
                city=temp2[0].strip()
                state=temp2[1].strip()
                thisgameinfo.append(city)
                thisgameinfo.append(state)
            except:
                thisgameinfo.append('')
                thisgameinfo.append('')
        else:
            thisgameinfo.append('')
            thisgameinfo.append('')
        return thisgameinfo
    
    def matchtimezone(self,thisgameinfo):
        Germantime=['Germany']
        Virgintime=['Virgin Islands','Puerto Rico','British Virgin Islands']
        Easterntime=['Mexico','Bahamas','ME','NH','MA','VT','RI','CT','NJ','PA','DE','DC','MD','VA','WV','OH','MI','IN','NC','SC','GA','FL','NY']
        Mountaintime=['MT','WY','CO','NM','ID','UT','AZ']
        Pacifictime=['WA','OR','CA','NV','BC']
        Centraltime=['ND','SD','MN','WI','IA','NE','KS','MO','IL','KY','TN','AL','AR','MS','LA','OK','TX']
        Hawaiitime=['HI']
        Altime=['AK']
        if thisgameinfo[-1] in Easterntime:
            thisgameinfo.append('0')
        elif thisgameinfo[-1] in Centraltime:
            thisgameinfo.append('1')
        elif thisgameinfo[-1] in Mountaintime:
            thisgameinfo.append('2')
        elif thisgameinfo[-1] in Pacifictime:
            thisgameinfo.append('3')
        elif thisgameinfo[-1] in Hawaiitime:
            thisgameinfo.append('5')
        elif thisgameinfo[-1] in Altime:
            thisgameinfo.append('4')
        elif thisgameinfo[-1] in Virgintime:
            thisgameinfo.append('-1')
        elif thisgameinfo[-1] in Germantime:
            thisgameinfo.append('-6')
        else:
            thisgameinfo.append('')
        if (thisgameinfo[-3]=='Lexington')and(thisgameinfo[-2]=='KY'):
            thisgameinfo[-1]=0
        if (thisgameinfo[-3]=='Puerto Vallarta')and(thisgameinfo[-2]=='Mexico'):
            thisgameinfo[-1]=1
        if (thisgameinfo[-3]=='Louisville')and(thisgameinfo[-2]=='KY'):
            thisgameinfo[-1]=0
        if (thisgameinfo[-3]=='Morehead')and(thisgameinfo[-2]=='KY'):
            thisgameinfo[-1]=0
        if (thisgameinfo[-3]=='Richmond')and(thisgameinfo[-2]=='KY'):
            thisgameinfo[-1]=0
        if (thisgameinfo[-3]=='Chattanooga')and(thisgameinfo[-2]=='TN'):
            thisgameinfo[-1]=0
        if (thisgameinfo[-3]=='Johnson City')and(thisgameinfo[-2]=='TN'):
            thisgameinfo[-1]=0
        if (thisgameinfo[-3]=='Knoxville')and(thisgameinfo[-2]=='TN'):
            thisgameinfo[-1]=0
        if (thisgameinfo[-3]=='Evansville')and(thisgameinfo[-2]=='IN'):
            thisgameinfo[-1]=1
        if (thisgameinfo[-3]=='Oakland City')and(thisgameinfo[-2]=='IN'):
            thisgameinfo[-1]=1
        if (thisgameinfo[-3]=='Valparaiso')and(thisgameinfo[-2]=='IN'):
            thisgameinfo[-1]=1
        if (thisgameinfo[-3]=='Moscow')and(thisgameinfo[-2]=='ID'):
            thisgameinfo[-1]=3
        return thisgameinfo
    
    def strip(self,address,startdatearray):
        fin=open(address,"r")
        aday=fin.read()
        fin.close()
        teamnames=findall("</td><td  align=left class=yspscores><b>(.+)</span>&nbsp;</td></tr>",aday)
        courtnames1=findall("<td height=20 class=yspscores>(.*)<br>",aday)
        cancelledcourtnames=findall("<td height=20 class=yspscores>(.*)<br>.*>Buy Tickets<",aday)
        self.gameinfo=[['','Away Team','AT 1st Half Score','AT 2nd Half Score','AT OT Score','AT Total Score','Home Team','HT 1st Half Score','HT 2nd Half Score','HT OT Score','HT Total Score','Home Court','City','State','Timezone']]
        aa=list(range(0,len(teamnames),2))
        courtnames=[]
        for item in courtnames1:
            if not(item in cancelledcourtnames):
                courtnames.append(item)
        for i in aa:
            nameaway=findall("class=yspmore>([a-zA-Z .\&\'\(\)\-]+)</a></b></td>",teamnames[i])
            if nameaway==[]:
                nameaway=findall("([a-zA-Z .\&\'\(\)\-]+)</b></td><td class=yspscores>",teamnames[i])
            namehome=findall("class=yspmore>([a-zA-Z .\&\'\(\)\-]+)</a></b></td>",teamnames[i+1])
            if namehome==[]:
                namehome=findall("([a-zA-Z .\&\'\(\)\-]+)</b></td><td class=yspscores>",teamnames[i+1])
            pointsawayst=findall(">([0-9]+)<",teamnames[i])
            pointshomest=findall(">([0-9]+)<",teamnames[i+1])
            if (pointsawayst!=[])and(pointshomest!=[]):
                pointsaway=[pointsawayst[0],pointsawayst[1],str(int(pointsawayst[-1])-int(pointsawayst[1])-int(pointsawayst[0])),pointsawayst[-1]]
                pointshome=[pointshomest[0],pointshomest[1],str(int(pointshomest[-1])-int(pointshomest[1])-int(pointshomest[0])),pointshomest[-1]]
                datest1=startdatearray[0]+'/'+startdatearray[1]+'/'+startdatearray[2]
                thisgameinfo=[datest1]
                thisgameinfo=self.thisgameinfo+nameaway+pointsaway+namehome+pointshome
                thisgameinfo.append(courtnames[int(i/2)])
                thisgameinfo=self.parenthesissep(thisgameinfo)
                thisgameinfo=self.matchtimezone(thisgameinfo)
                self.gameinfo.append(thisgameinfo)
    
    def csvOutput(self,address):
        fout=open(address[:-5]+".csv","w",newline="")
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(self.gameinfo)
        fout.close()
    
    def transformDay(self,dated):
        year=str(dated.year)
        month=str(dated.month)
        day=str(dated.day)
        try:
            datest=year+'-'+month+'-'+day
            address=datest+'.source.html'
            self.strip(address,[month,day,year])
            self.csvOutput(address)
        except:
            messagebox.showerror("Error","Please enter a valid path and valid dates")
            raise ValueError
    
    def checkIn(gameinfo,csvFilename):
        dateArray=gameinfo[1][1]
        try:
            fin=open(csvFilename,'r')
            csvReadert=csv.reader(fin)
            self.matchinfo=[]
            for item in csvReadert:
                if item != []:
                    self.matchinfo.append(item)
            if self.matchinfo == []:
                for item in gameinfo:
                    self.matchinfo.append(item)
                print("This day has not been recorded to the file")
            else:
                counter=0
                for item in self.matchinfo[1:]:
                    st=item[0]
                    datearray=st.split('/')
                    if int(datearray[2])>int(dateArray[0]):
                        break
                    elif int(datearray[0])>int(dateArray[1]):
                        break
                    elif int(datearray[1])>int(dateArray[2]):
                        break
                    else:
                        if [int(datearray[2]),int(datearray[0]),int(datearray[1])]==[int(dateArray[0]),int(self.dateArray[1]),int(dateArray[2])]:
                            print("This day has already been recorded to the file")
                            return
                        else:
                            counter=counter+1;
                self.matchinfo=self.matchinfo[:counter+1]+gameinfo[1:]+self.matchinfo[counter+1:len(self.matchinfo)]
                print("This day has not been recorded to the file")
        except:
            messagebox.showwarning("Error","Error.")
            return
    
    def realAppend(matchinfo,csvFilename):
        fout=open(csvFilename,"w",newline="")
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(matchinfo)
        fout.close()
    
    def appendDay(self,gameinfo,csvFilename):
        self.checkIn(gameinfo,csvFilename)
        self.realAppend(self.matchinfo,csvFilename)
    
    def buttonCompile(self):
        self.inputDate()
        currentDate=self.startDated
        while currentDate<=self.endDated:
            self.gameinfo=[]
            self.extractDay(currentDate)
            self.transformDay(currentDate)
            self.appendDay(self.gameinfo,csvFilename)
            currentDate=currentDate+timedelta(1)
    
    def importBid(year):
        fin=open("Bidsinfo"+year[-2:]+".csv","r")
        csvReader=csv.reader(fin)
        self.bidsInfo={}
        for item in csvReader:
            self.bidsInfo[item[0]]=item[3]
        fin.close()
    
    def importTeam():
        try:
            year=self.yearstr.get()
            yearshort=year[-2:]
            csvReader=csv.reader("teams"+yearshort+".csv")
            counter=0
            self.conference={}
            self.court={}
            self.city={}
            self.state={}
            self.timezone={}
            self.latitude={}
            self.longitude={}
            self.elevation={}
            for item in csvReader:
                if counter==0:
                    counter=counter+1
                else:
                    self.conference[item[0]]=item[4]
                    self.court[item[0]]=item[1]
                    self.city[item[0]]=item[2]
                    self.state[item[0]]=item[3]
                    self.timezone[item[0]]=item[5]
                    self.latitude[item[0]]=item[6]
                    self.longitude[item[0]]=item[7]
                    self.elevation[item[0]]=item[8]
        except:
            fin=open('teams'+year+'.txt','r')
            st=fin.read()
            fin.close()
            stadium=findall('([A-Za-z .&\-\'\(\)]+)\t([0-9\-]+)\t(.+) \((.+), (.+)\)',st)
            stadiumnone=findall('([A-Za-z .&\-\']+)\t([0-9\-]+)\t([noe]+)',st)
            i=0
            data=[]
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
            fout=open('teams'+year+'.csv','w',newline="")
            csvWriter=csv.writer(fout,dialect="")
            csvWriter.writerows(data)
            fout.close()
            
    def buttonGeneratefinal(self):
        self.importBid(self.yearstr)
        self.importTeam(self.yearstr)
        self.finalsheetMaker()
            
    def changeDir(self,path):
        os.chdir(path)
    
    def __init__(self):
        # GUIs going in here
        a=a+1
 