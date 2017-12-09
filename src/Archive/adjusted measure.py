# Linear Regression over Adjusted Measure of Points Difference
# 2/26/2014

import csv
import os
os.chdir("C:\\Documents\\ISYE\\Research\\Data and Spreadsheets")
import numpy as np
from scipy import stats
import math
from operator import *

class Adjmeasure:
    def importTeam(self,year):
        fin=open("Teams names and numbers.csv","r")
        csvReader=csv.reader(fin)
        index=0
        self.teamDict={}
        self.teamMat=[]
        for item in csvReader:
            if index==0:
                for i in range(len(item)):
                    if int(item[i])==year:
                        column=i
                index=index+1
            else:
                if item[column]!='':
                    self.teamDict[item[column]]=item[len(item)-1]
                self.teamMat.append(0)
        fin.close()
        
    def importYear(self,year):
        yearstr=str(year)
        address="Finalspreadsheet"+yearstr[-2:]+".csv"
        fin=open(address,"r")
        csvReader=csv.reader(fin)
        self.y=[]
        self.x=[]
        for item in csvReader:
            pointDiff=int(item[28])
            self.y.append(agDict[pointDiff]-4)
            line=self.teamMat.copy()
            line[self.teamDict[item[1]]]=-1
            line[self.teamDict[item[12]]]=1
            self.x.append(line)
    
    def regressionYear(self,x,y):
        ones = np.ones(len(x[0]))
        X = sm.add_constant(np.column_stack((x[0], ones)))
        for ele in x[1:]:
            X = sm.add_constant(np.column_stack((ele, X)))
        results = sm.OLS(y, X).fit()
        return results
        
        
    def regressionYear(self,year):
        self.importTeam(year)
        self.importYear(year)
        self.regressionAct(self.x,self.y)
        
    
    def __init__(self,year):
        # Read in the final spreadsheet file
        fin=open("Adjusted.csv","r")
        csvReader=csv.reader(fin)
        index=0
        agDict={}
        for item in csvReader:
            if index==0:
                index=index+1
                for yearindex in range(1,len(item)):
                    if str(year) in item[yearindex]:
                        colindex=yearindex
            else:
                agDict[int(item[0])]=float(item[colindex])
        fin.close()