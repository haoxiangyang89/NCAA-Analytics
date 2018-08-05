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
        self.gdate = gdate
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
    totalData = np.array([])
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
        
        h3ptPerc = float(item[title.index("Home 3PT Percentage")])
        a3ptPerc = float(item[title.index("Away 3PT Percentage")])
        h2ptPerc = (hFGmade - h3ptmade)/(hFGattempt - h3ptattempt)
        a2ptPerc = (aFGmade - a3ptmade)/(aFGattempt - a3ptattempt)
        
        hFTPerc = float(item[title.index("Home FT Percentage")])
        aFTPerc = float(item[title.index("Away FT Percentage")])
        
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
        if totalData.size == 0:
            totalData = np.array([gamestat])
        else:
            totalData = np.append(totalData,np.array([gamestat]),axis = 0)
        
    return teamID,dataList,totalData

def bayesLearn(teamID,dataList):
    # artificial variance
    avgStat = np.mean(totalData,axis = 0)
    varStat = avgStat*0.05
    varMat = np.diag(varStat**2)
    
    # initialization with every team's theta prior
    thetaDict = {}
    for tID in teamID.keys():
        thetaDict[tID] = np.array([])