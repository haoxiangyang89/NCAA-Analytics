# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# NCAA Scraper
# this is the demonstration for Git Commit

import os
import csv
import re
import urllib.request
from selenium import webdriver
from urllib.request import FancyURLopener

import pdb
pdb.set_trace()

import json
import datetime
import time
import bs4

class NCAAScraper:
    # Get the list of game ids
    def GetGameList(self):
        currentDate = self.start
        self.totalGameList = {}
        browser = webdriver.Chrome("/Users/haoxiangyang/Downloads/chromedriver") # change it to your own chromedriver address
        time.sleep(10)
        while currentDate <= self.end:
            
            # Here we use selenium to obtain the list of the games
            yearDig = str(currentDate.year)
            if currentDate.month < 10:
                monthDig = self.digTrans[currentDate.month]
            else:
                monthDig = str(currentDate.month)
            if currentDate.day < 10:
                dayDig = self.digTrans[currentDate.day]
            else:
                dayDig = str(currentDate.day)
            browser.get('http://www.espn.com/mens-college-basketball/scoreboard/_/group/50/date/{}{}{}'.format(yearDig,monthDig,dayDig))
            time.sleep(10)
            elemList = browser.find_elements_by_class_name('mobileScoreboardLink')
            addressList = []
            for i in range(0,len(elemList)):
                address = elemList[i].get_attribute("href")
                addressList.append(address)
            self.totalGameList[currentDate] = addressList
            currentDate = currentDate + datetime.timedelta(1)
            
    def GetDataList(self):
        header = ["Team Name","Home","FG Made","FG Attempt","3PT Made","3PT Attempt","FT Made","FT Attempt",\
                  "OREB","DREB","REB","AST","STL","BLK","TO","PF","PTS"]
        
        # scrape the data from espn.com
        currentDate = self.start
        browser = webdriver.Chrome("/Users/haoxiangyang/Downloads/chromedriver") # change it to your own chromedriver address
        while currentDate <= self.end:
            for igame in self.totalGameList[currentDate]:
                # find the patterns and scrape the data
                # Please try to finish this part of the code
    
    # Print the collected data into a csv file
    def Output(self):
        if self.existed:
            self.fo = open(self.fileOutput,'a',newline = '')
            self.csvWriter = csv.writer(self.fo,dialect = 'excel')
        else:
            self.fo = open(self.fileOutput,'w',newline = '')
            self.csvWriter = csv.writer(self.fo,dialect = 'excel')
        self.csvWriter.writerows(self.gameList)
        self.fo.close()
            
    def __init__(self,start,end,fileOutput):
        startList = start.split(".")
        endList = end.split(".")
        self.digTrans = {1:'01',2:'02',3:'03',4:'04',5:'05',6:'06',7:'07',8:'08',9:'09'}
        self.fileOutput = fileOutput
        self.start = datetime.date(int(startList[0]),int(startList[1]),int(startList[2]))
        self.end = datetime.date(int(endList[0]),int(endList[1]),int(endList[2]))
        if os.path.exists(self.fileOutput):
            self.existed = True
        else:
            self.existed = False