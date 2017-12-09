# Code based on Massey's Data for QUEST Practice
# 3/26/2014
import os
import csv
import urllib.request
from re import findall
from tkinter import *
from operator import *
from datetime import *

class MasseyDatacompiler:
    
    def convertDate2(self,datee):
        array=datee.split('-')
        return date(year=int(array[0]),month=int(array[1]),day=int(array[2]))
    
    def spaceReplacer(self,tstring):
        if tstring.find('_')==-1:
            return tstring
        else:
            return tstring[:tstring.find('_')]+' '+self.spaceReplacer(tstring[tstring.find('_')+1:])
    
    def readTeams(self,year):
        address='http://www.masseyratings.com/scores.php?s='+self.yearCode[year]+'&sub=11590&all=1&mode=3&exhib=on&format=2'
        webFile=urllib.request.urlopen(address)
        st=webFile.read()
        st=st.decode("utf-8")
        teamRaw=st.split('\n')
        self.teamNo={}
        self.teamNorev={}
        for item in teamRaw:
            if item!='':
                item=item.strip()
                teamNoname=item.split(',')
                teamNo=teamNoname[0]
                temp=teamNoname[1].strip()
                teamName=self.spaceReplacer(temp)
                self.teamNo[teamName]=int(teamNo)
                self.teamNorev[int(teamNo)]=teamName
        webFile.close()
    
    def readConference(self,year):
        webFile=urllib.request.urlopen(self.matchst)
        st=webFile.read()
        Orist=st.decode("utf-8")
        conference=findall('\n <a href="scores.php\?s='+self.yearCode[self.year]+'&sub=([0-9]+)">([0-9a-zA-Z \-]+)</a> \|',Orist)
        self.teamConf={}
        for item in conference:
            confstr='http://www.masseyratings.com/scores.php?s='+self.yearCode[self.year]+'&sub='+item[0]+'&all=1&mode=3&exhib=on&format=2'
            webFile1=urllib.request.urlopen(confstr)
            teamst=webFile1.read()
            teamst=teamst.decode("utf-8")
            teamRaw=teamst.split('\n')
            for item1 in teamRaw:
                if item1!='':
                    item1=item1.strip()
                    teamNoname=item1.split(',')
                    temp=teamNoname[1].strip()
                    teamName=self.spaceReplacer(temp)
                    self.teamConf[teamName]=item[1]
            webFile1.close()
        webFile.close()
        
    def readMatch(self,year):
        webFile=urllib.request.urlopen(self.matchst)
        st=webFile.read()
        Orist=st.decode("utf-8")
        match=findall('([0-9\-]+)([a-zA-z \@\.\&\'\(\)\-]+)([0-9]+)([a-zA-z \@\.\&\'\(\)\-]+)([0-9]+)(.+)\n',Orist)
        self.matchraw=[]
        for item in match:
            temp=list(item)
            temp[0]=self.convertDate2(temp[0])
            temp[1]=temp[1].strip()
            temp[3]=temp[3].strip()
            temp[2]=int(temp[2])
            temp[4]=int(temp[4])
            temp[5]=temp[5][2:].strip()
            if (temp[0]>=self.startDate)and(temp[0]<=self.endDate):
                self.matchraw.append(temp)
    
    def compileMatch(self,year,matchraw):
         try:
            self.matchHA=[]
            for item in matchraw:
                temp=[]
                temp.append(item[0])
                if item[1][0]=='@':
                    temp.append(item[1][1:])
                    temp.append(item[2])
                    temp.append(self.teamConf[item[1][1:]])
                    temp.append(item[3])
                    temp.append(item[4])
                    temp.append(self.teamConf[item[3]])
                    temp.append(item[5])
                    temp.append(temp[2]-temp[5])
                    temp.append(0)
                elif item[3][0]=='@':
                    temp.append(item[3][1:])
                    temp.append(item[4])
                    temp.append(self.teamConf[item[3][1:]])
                    temp.append(item[1])
                    temp.append(item[2])
                    temp.append(self.teamConf[item[1]])
                    temp.append(item[5])
                    temp.append(temp[2]-temp[5])
                    temp.append(0)
                else:
                    temp.append(item[1])
                    temp.append(item[2])
                    temp.append(self.teamConf[item[1]])
                    temp.append(item[3])
                    temp.append(item[4])
                    temp.append(self.teamConf[item[3]])
                    temp.append(item[5])
                    temp.append(temp[2]-temp[5])
                    temp.append(1)
                if temp[3]==temp[6]:
                    temp.append(1)
                else:
                    temp.append(0)
                self.matchHA.append(temp)
         except:
             print("Error")
    
    def changedir(self,dirr):
        os.chdir(dirr)
    
    def printCSV(self,year):
        title=['Date','Home Team','Home Team Score','Home Team Conference','Away Team','Away Team Score','Away Team Conference','Match Notes','Point Difference','Neutral Game?','Conference Game?']
        printout=[title]+self.matchHA
        fout=open("Massey"+str(year)+".csv",'w',newline="")
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(printout)
        fout.close()
    
    def printTeam(self):
        self.teamNotot={}
        maxx=0
        for item in range(2000,2015):
            self.readTeams(item)
            self.teamNotot[item]=self.teamNorev
            if maxx<=len(self.teamNorev):
                maxx=len(self.teamNorev)
        printoutdata=[["Number","Team"]*15]
        for i in range(1,maxx+1):
            temp=[]
            for year1 in range(2000,2015):
                if i in self.teamNotot[year1].keys():
                    temp.append(i)
                    temp.append(self.teamNotot[year1][i])
                else:
                    temp.append('')
                    temp.append('')
            printoutdata.append(temp)
        fout=open("Teams names and numbers New.csv","w",newline="")
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(printoutdata)
            
    
    def executeCompiler(self,year,dirr):
        self.changedir(dirr)
        self.readConference(year)
        self.readMatch(year)
        self.compileMatch(year,self.matchraw)
        self.printCSV(year)
        
    def __init__(self,year,startDate,endDate):
        self.year=year
        self.yearCode={2014:'203290',2013:'193573',2012:'179268',2011:'101140',2010:'97288',2009:'87798',2008:'74994',2007:'69587',2006:'41469',2005:'41468',2004:'41467',2003:'41466',2002:'41465',2001:'41464',2000:'41463'}
        self.matchst='http://www.masseyratings.com/scores.php?s='+self.yearCode[year]+'&sub=11590&all=1&mode=2&exhib=on&format=0'
        self.startDate=self.convertDate2(startDate)
        self.endDate=self.convertDate2(endDate)