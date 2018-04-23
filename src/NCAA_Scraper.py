# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# NCAA Scraper
# this is the demonstration for Git Commit

import os
import csv
import copy
import urllib.request
from selenium import webdriver
from urllib.request import FancyURLopener

#import pdb
#pdb.set_trace()

import datetime
import time
import bs4

class NCAAScraper:
    # Get the list ofa =  game ids
    def GetGameList(self):
        currentDate = self.start
        self.totalGameList = {}
        browser = webdriver.Chrome("C:\\Users\\hyang89\\Documents\\Git\\chromedriver_win32\\chromedriver.exe") # change it to your own chromedriver address
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
            addressList = []
            # Here group 50 has some missing matches on some days
            # So we have to examine every conference's schedule
            for cid in self.confID:
                browser.get('http://www.espn.com/mens-college-basketball/scoreboard/_/group/{}/date/{}{}{}'.format(cid,yearDig,monthDig,dayDig))
                time.sleep(5)
                elemList = browser.find_elements_by_class_name('mobileScoreboardLink')
                for i in range(0,len(elemList)):
                    address = elemList[i].get_attribute("href")
                    if not(address in addressList):
                        addressList.append(address)
            self.totalGameList[currentDate] = addressList
            currentDate = currentDate + datetime.timedelta(1)
            
    def GetData(self):
        header = ["Date","Home Team Name","Away Team Name","Home Team ID","Away Team ID","Neutral","Location","Zipcode","Tournament","Special",\
                  "Home FG Made","Away FG Made","Home FG Attempt","Away FG Attempt","Home FG Percentage","Away FG Percentage",\
                  "Home 3PT Made","Away 3PT Made","Home 3PT Attempt","Away 3PT Attempt","Home 3PT Percentage","Away 3PT Percentage",\
                  "Home FT Made","Away FT Made","Home FT Attempt","Away FT Attempt","Home FT Percentage","Away FT Percentage",\
                  "Home OREB","Away OREB","Home DREB","Away DREB","Home TREB","Away TREB","Home REB","Away REB","Home AST","Away AST",\
                  "Home STL","Away STL","Home BLK","Away BLK","Home TO","Away TO","Home PF","Away PF","Home TF","Away TF",\
                  "Home FF","Away FF","Home PTS","Away PTS"]
        self.totalData = [header]
        # scrape the data from espn.com
        currentDate = self.start
        while currentDate <= self.end:
            for igame in self.totalGameList[currentDate]:
                try:
                    igameM = copy.copy(igame)
                    igameM = igame.replace("game?","matchup?")
                    # find the teams' name/ID/the location of game
                    basicFile = urllib.request.urlopen(igame)
                    basicString = basicFile.read()
                    basicString = basicString.decode("utf-8")
                    # BeautifulSoup information: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
                    basicSoup = bs4.BeautifulSoup(basicString,'html.parser')
                    # location of the game
                    locationObj = basicSoup.find("div",attrs={"class":"location-details"})
                    location = locationObj.ul.li.contents[0].strip()
                    zipcode = locationObj.ul.li.span.contents[0].strip()
                    # special notes of the game
                    if basicSoup.find("div",attrs={"class":"game-details header"}) == None:
                        matchNotes = ""
                    else:
                        matchNotes = basicSoup.find("div",attrs={"class":"game-details header"}).contents[0]
                    # neutral game or not
                    recordList = basicSoup.findAll("div",attrs={"class":"record"})
                    recordText = recordList[0].text + recordList[1].text
                    if matchNotes != "":
                        # To check whether it is a special event/determine whether it is a neutral game
                        if ("TOURNAMENT" in matchNotes)or("CONFERENCE" in matchNotes)or("CHAMPIONSHIP" in matchNotes):
                            neutralBool = True
                            tourBool = True
                            specialBool = False
                        else:
                            tourBool = False
                            specialBool = True
                            if ("Home" in recordText)or("Away" in recordText):
                                neutralBool = False
                            else:
                                neutralBool = True
                    else:
                        tourBool = False
                        specialBool = False
                        if ("Home" in recordText)or("Away" in recordText):
                            neutralBool = False
                        else:
                            neutralBool = True
                    teamInfo = basicSoup.findAll("div",attrs={"class":"team-info-wrapper"})
                    atName = teamInfo[0].find("span",attrs={"class":"long-name"}).text
                    if teamInfo[0].a != None:
                        atID = int(teamInfo[0].a.attrs['data-clubhouse-uid'].split(":")[-1])
                    else:
                        atID = 99999
                    htName = teamInfo[1].find("span",attrs={"class":"long-name"}).text
                    if teamInfo[1].a != None:
                        htID = int(teamInfo[1].a.attrs['data-clubhouse-uid'].split(":")[-1])
                    else:
                        htID = 99999
                    # Some games are postponed, this condition is to deal with that
                    if basicSoup.findAll(name = "td",attrs={"class":"final-score"}) != []:
                        awayPTS = int(basicSoup.findAll(name = "td",attrs={"class":"final-score"})[0].text)
                        homePTS = int(basicSoup.findAll(name = "td",attrs={"class":"final-score"})[1].text)
                        
                        # obtain the team data by Soup
                        statFile = urllib.request.urlopen(igameM)
                        statString = statFile.read()
                        statString = statString.decode("utf-8")
                        statSoup = bs4.BeautifulSoup(statString,'html.parser')
                        teamData = statSoup.findAll(name = "tr",attrs = {"class":["highlight","indent"]})
                        for item in teamData:
                            dataList = item.findAll("td")
                            dataName = dataList[0].text.strip()
                            dataAway = dataList[1].text.strip()
                            dataHome = dataList[2].text.strip()
                            if dataName == "FG Made-Attempted":
                                awayFGM = int(dataAway.split("-")[0])
                                awayFGA = int(dataAway.split("-")[1])
                                homeFGM = int(dataHome.split("-")[0])
                                homeFGA = int(dataHome.split("-")[1])
                            if dataName == "Field Goal %":
                                awayFGP = float(dataAway)
                                homeFGP = float(dataHome)
                            if dataName == "3PT Made-Attempted":
                                away3PTM = int(dataAway.split("-")[0])
                                away3PTA = int(dataAway.split("-")[1])
                                home3PTM = int(dataHome.split("-")[0])
                                home3PTA = int(dataHome.split("-")[1])
                            if dataName == "Three Point %":
                                away3PTP = float(dataAway)
                                home3PTP = float(dataHome)
                            if dataName == "FT Made-Attempted":
                                awayFTM = int(dataAway.split("-")[0])
                                awayFTA = int(dataAway.split("-")[1])
                                homeFTM = int(dataHome.split("-")[0])
                                homeFTA = int(dataHome.split("-")[1])
                            if dataName == "Free Throw %":
                                awayFTP = float(dataAway)
                                homeFTP = float(dataHome)
                            if dataName == "Total Rebounds":
                                awayREB = int(dataAway)
                                homeREB = int(dataHome)
                            if dataName == "Offensive Rebounds":
                                awayOREB = int(dataAway)
                                homeOREB = int(dataHome)
                            if dataName == "Defensive Rebounds":
                                awayDREB = int(dataAway)
                                homeDREB = int(dataHome)
                            if dataName == "Team Rebounds":
                                awayTREB = int(dataAway)
                                homeTREB = int(dataHome)
                            if dataName == "Assists":
                                awayAST = int(dataAway)
                                homeAST = int(dataHome)
                            if dataName == "Steals":
                                awaySTL = int(dataAway)
                                homeSTL = int(dataHome)
                            if dataName == "Blocks":
                                awayBLK = int(dataAway)
                                homeBLK = int(dataHome)
                            if dataName == "Total Turnovers":
                                awayTO = int(dataAway)
                                homeTO = int(dataHome)
                            if dataName == "Personal Fouls":
                                awayPF = int(dataAway)
                                homePF = int(dataHome)
                            if dataName == "Technical Fouls":
                                awayTF = int(dataAway)
                                homeTF = int(dataHome)
                            if dataName == "Flagrant Fouls":
                                awayFF = int(dataAway)
                                homeFF = int(dataHome)
                        
                        # consolidate the game data and append it to the totalData list
                        gameData = ["{}-{}-{}".format(currentDate.year,currentDate.month,currentDate.day),htName,atName,\
                            htID,atID,neutralBool,location,zipcode,tourBool,specialBool,\
                            homeFGM,awayFGM,homeFGA,awayFGA,homeFGP,awayFGP,home3PTM,away3PTM,home3PTA,away3PTA,\
                            home3PTP,away3PTP,homeFTM,awayFTM,homeFTA,awayFTA,homeFTP,awayFTP,\
                            homeOREB,awayOREB,homeDREB,awayDREB,homeTREB,awayTREB,homeREB,awayREB,\
                            homeAST,awayAST,homeSTL,awaySTL,homeBLK,awayBLK,homeTO,awayTO,homePF,awayPF,\
                            homeTF,awayTF,homeFF,awayFF,homePTS,awayPTS]
                        self.totalData.append(gameData)
                except:
                    print(igame+"\n")
            currentDate = currentDate + datetime.timedelta(1)
        
    
    # Print the collected data into a csv file
    def Output(self):
        if self.existed:
            self.fo = open(self.fileOutput,'a',newline = '')
            self.csvWriter = csv.writer(self.fo,dialect = 'excel')
        else:
            self.fo = open(self.fileOutput,'w',newline = '')
            self.csvWriter = csv.writer(self.fo,dialect = 'excel')
        self.csvWriter.writerows(self.totalData)
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
        # the group number of each conference
        self.confID = [3,46,2,1,62,8,4,5,6,7,9,11,10,45,12,13,14,16,18,44,19,20,21,22,23,26,24,25,49,27,30,29]