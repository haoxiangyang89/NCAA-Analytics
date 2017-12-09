# Logistics Regression Model
# 2/9/2014

from numpy import *
from scipy import *
import csv
from operator import *
import os
os.chdir("C:\Documents\ISYE\Research\Massey Data")

class logRegression:
    
    def logregCore(self,startingyear):
        self.regressiontable[startingyear]=[]
        for i in range (4):
            yearstr=str(startingyear+i)
            address="Massey"+yearstr+".csv"
            fin=open(address,'r')
            csvReader=csv.reader(fin)
        
            # read in the match entries that are conference games and played at the regular/secondary home court
            # conference tournament not included
            data=[]
            for item in csvReader:
                if (item[9]=='0')and(item[10]=='1'):
                    data.append(item)
            fin.close()
        
            # initialization before iteration on data, set up a set for matches to be marked
            mark=[]
            for j in range(len(data)):
                mark.append(0)
            # iteration
            index=0
            for item in data:
                if mark[index]==0:              #not marked
                    pointdiff=item[8]
                    for j in range(index+1,len(data)):
                        if (data[j][1]==item[4])and(data[j][4]==item[1]):
                            if float(data[j][8])>=0:
                                self.regressiontable[startingyear].append([pointdiff,0])
                            else:
                                self.regressiontable[startingyear].append([pointdiff,1])
    
    def printRegtable(self,startingyear):
        # ouput
        fout=open("regressiontable"+str(startingyear+3)+".csv",'w',newline="")
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(self.regressiontable[startingyear])
        fout.close()
        
            
    def executeLogreg(self):
        # initialization: build the table with legend of points difference
        startingyear=2000
        while startingyear<=2011:
            self.logregCore(startingyear)
            self.printRegtable(startingyear)
            self.printRegtable(startingyear)
            startingyear=startingyear+1
    
    def __init__(self):
        self.regressiontable={}
