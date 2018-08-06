#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 21:39:43 2018

@author: haoxiangyang
"""

import os
import csv
import copy
import numpy as np
import scipy
import datetime
import sklearn

class dataEntry:
    def __init__(self,gdate,hTeam,aTeam,neutral,specTour,confTour,gameStat):
        self.gDate = gdate
        self.hTeam = hTeam
        self.aTeam = aTeam
        self.neutral = neutral
        self.specTour = specTour
        self.confTour = confTour
        self.gameStat = gameStat

# function to read in the data from csv and store them
def readRaw(address):
    fi = open(address,"r")
    csvReader = csv.reader(fi)
    gameList = []
    counter = 1
    for item in csvReader:
        if counter == 1:
            title = item
            counter += 1
        else:
            gameList.append(item)
    fi.close()
    return title,gameList

def parseRaw(title,gameList):
    # capture all team's id
    teamID = {}
    for item in gameList:
        homeID = int(item[title.index("Home Team ID")])
        homeName = item[title.index("Home Team Name")]
        if homeID in teamID.keys():
            if homeName != teamID[homeID]:
                print(homeName,homeID)
        else:
            teamID[homeID] = homeName
        
        awayID = int(item[title.index("Away Team ID")])
        awayName = item[title.index("Away Team Name")]
        if awayID in teamID.keys():
            if awayName != teamID[awayID]:
                print(awayName,awayID)
        else:
            teamID[awayID] = awayName
    
    gameID = 0
    dataList = []
    for item in gameList:
        dataItem = []
        
        gameID += 1
        dataItem.append(gameID)
        
        dateStr = item[0].split("/")
        gameDate = datetime.date(2000 + int(dateStr[2]), int(dateStr[0]),int(dateStr[1]))
        
        homeID = int(item[title.index("Home Team ID")])
        awayID = int(item[title.index("Away Team ID")])
        if item[title.index("Neutral")] == "TRUE":
            neutral = True
        else:
            neutral = False
        if item[title.index("Special")] == "TRUE":
            specTour = True
        else:
            specTour = False
        if item[title.index("Tournament")] == "TRUE":
            confTour = True
        else:
            confTour = False
            
        hFGattempt = int(item[title.index("Home FG Attempt")])
        aFGattempt = int(item[title.index("Away FG Attempt")])
        h3ptattempt = int(item[title.index("Home 3PT Attempt")])
        a3ptattempt = int(item[title.index("Away 3PT Attempt")])
        
        hFGmade = int(item[title.index("Home FG Made")])
        aFGmade = int(item[title.index("Away FG Made")])
        h3ptmade = int(item[title.index("Home 3PT Made")])
        a3ptmade = int(item[title.index("Away 3PT Made")])
        
        h3ptPerc = float(item[title.index("Home 3PT Percentage")])/100
        a3ptPerc = float(item[title.index("Away 3PT Percentage")])/100
        h2ptPerc = (hFGmade - h3ptmade)/(hFGattempt - h3ptattempt)
        a2ptPerc = (aFGmade - a3ptmade)/(aFGattempt - a3ptattempt)
        
        hFTPerc = float(item[title.index("Home FT Percentage")])/100
        aFTPerc = float(item[title.index("Away FT Percentage")])/100
        
        hFoul = int(item[title.index("Home PF")])
        aFoul = int(item[title.index("Away PF")])
        
        hTO = int(item[title.index("Home TO")])
        aTO = int(item[title.index("Away TO")])
        
        hBLK = int(item[title.index("Home BLK")])
        aBLK = int(item[title.index("Away BLK")])
        
        hOREB = int(item[title.index("Home OREB")])
        aOREB = int(item[title.index("Away OREB")])
        hDREB = int(item[title.index("Home DREB")])
        aDREB = int(item[title.index("Away DREB")])
        hREBratio = hOREB/(hOREB + aDREB)
        aREBratio = aOREB/(aOREB + hDREB)
        
        gamestat = np.array([hFGattempt,aFGattempt,h2ptPerc,a2ptPerc,h3ptPerc,a3ptPerc,hFTPerc,aFTPerc,\
                             hFoul,aFoul,hTO,aTO,hBLK,aBLK,hREBratio,aREBratio])
        
        dataItem = dataEntry(gameDate,homeID,awayID,neutral,specTour,confTour,gamestat)
        dataList.append(dataItem)
      
    dataList = sorted(dataList,key = lambda k:k.gDate)
    totalData = np.array([])
    for item in dataList:
        if totalData.size == 0:
            totalData = np.array([item.gameStat])
        else:
            totalData = np.append(totalData,np.array([item.gameStat]),axis = 0)
        
    return teamID,dataList,totalData

def bayesLearn(teamID,dataList,totalData):
    # artificial variance
    avgStat = np.mean(totalData,axis = 0)
    varStat = avgStat*0.05
    varMat = np.diag(varStat**2)
    
    # initialization with every team's theta prior
    thetamDict = {}
    thetasDict = {}
    OCA = (avgStat[0] + avgStat[1])/2
    OSA = 0
    twoAccu = (avgStat[2] + avgStat[3])/2
    twoD = 0
    threeAccu = (avgStat[4] + avgStat[5])/2
    threeD = 0
    ftAccu = (avgStat[6] + avgStat[7])/2
    FCA = (avgStat[8] + avgStat[9])/2
    DC = 0
    TOCA = (avgStat[10] + avgStat[11])/2
    PTO = (avgStat[10] + avgStat[11])/2
    BLKA = (avgStat[12] + avgStat[13])/2
    PBLK = (avgStat[12] + avgStat[13])/2
    ORA = (avgStat[14] + avgStat[15])/2
    DRA = 0
    
    for tID in teamID.keys():
        thetamDict[tID] = np.array([OCA,OSA,twoAccu,twoD,threeAccu,threeD,ftAccu,FCA,DC,\
                 TOCA,PTO,BLKA,PBLK,ORA,DRA])
        thetasDict[tID] = np.array([OCA*0.05,OCA*0.05,twoAccu*0.05,twoAccu*0.05,threeAccu*0.05,threeAccu*0.05,\
                  ftAccu*0.05,FCA*0.05,FCA*0.05,TOCA*0.05,PTO*0.05,BLKA*0.05,PBLK*0.05,ORA*0.05,ORA*0.05])**2
    
    A = np.matrix([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                  [0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                  [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0],\
                  [0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],\
                  [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],\
                  [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],\
                  [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],\
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1],\
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]])
    
    # Bayesian learning process
    for item in dataList:
        # update the variance for the theta
        joints = np.append(thetasDict[item.hTeam],thetasDict[item.aTeam])
        sigma = np.linalg.inv(np.linalg.inv(np.diag(joints))+np.transpose(A)*np.linalg.inv(varMat)*A)
        thetasDict[item.hTeam] = sigma[:14,:14]
        thetasDict[item.aTeam] = sigma[15:,15:]
        
        # update the mean for the theta
        jointm = np.append(thetamDict[item.hTeam],thetamDict[item.aTeam])
        mu = sigma*(jointm*np.linalg.inv(np.diag(joints))+np.transpose(A)*np.linalg.inv(varMat)*item.gameStat)
        thetamDict[item.hTeam] = mu[:14]
        thetamDict[item.aTeam] = mu[15:]