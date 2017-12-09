import csv

for i in range(2013,2014):
    a=str(i)
    yearshort=a[2:]
    #print(yearshort)
    finmatch=open('D:\\Matchinfo\\'+a+' with courtinfo.csv','r')
    finteam=open('D:\\Teamstadiums\\teams'+yearshort+'.csv','r')
    finbids=open('D:\\Matchinfo\\Bidsinfo'+yearshort+'.csv','r')
    csvReader1=csv.reader(finmatch)
    csvReader2=csv.reader(finteam)
    csvReader3=csv.reader(finbids)
    matchinfo=[]
    teaminfo={}
    teamtimezoneinfo={}
    teamstadiuminfo={}
    teamconferenceinfo={}
    total=[['Date','Away Team Name','AT 1st Half Score','AT 2nd Half Score','AT OT Score','AT Total Score','AT Timezone East','AT Timezone West','Away Team Latitude','Away Team Longitude','AT distance','AT conference',
            'Home Team Name','HT 1st Half Score','HT 2nd Half Score','HT OT Score','HT Total Score','HT Timezone East','HT Timezone West','Home Team Latitude','Home Team Longitude','HT distance','HT conference',
            'Court Played on','City Played in','State Played in','Timezone played in','Game Info','Score Differential',
            'Average NCAA bids% Differential','Conference Game','Conference Tournament','Special Tournament','Regular Homecourt',
            'Secondary Homecourt','Neutral Game','Equidistant to Both','Close to Away',
            'Awayteam bids\%','Hometeam bids\%']]
    for item in csvReader1:
        matchinfo.append(item)
        #print(item[5])
    matchinfo=matchinfo[1:]
    #print(matchinfo)
    teamname=[]
    for item in csvReader2:
        try:
            #print(item)
            teamtimezoneinfo[item[0]]=item[5]
            teamconferenceinfo[item[0]]=item[4]
            teamstadiuminfo[item[0]]=item[1]
            teamname.append(item[0])
        except:
            pass
    conferencebids={}
    for item in csvReader3:
        try:
            conferencebids[item[0]]=float(item[3])
        except:
            pass
    total[0]=total[0]+teamname
    #print(teamtimezoneinfo)
    #print(yearshort)
    for item in matchinfo:
        if '<br>' in item[11]:
            a=item[11].split('<br>')
            item[11]=a[1]
            item.append(a[0])
        else:
            item.append('')
        if (item[1] in teamtimezoneinfo.keys())and(item[14]!='')and(teamtimezoneinfo[item[1]]!=''):
            ATtzdifference=(int(teamtimezoneinfo[item[1]])-int(item[14]))
            if ATtzdifference<0:
                ATwest=str(abs(ATtzdifference))
                ATeast='0'
            else:
                ATeast=str(ATtzdifference)
                ATwest='0'
        else:
            ATeast='NULL'
            ATwest='NULL'
        if (item[6] in teamtimezoneinfo.keys())and(item[14]!='')and(teamtimezoneinfo[item[6]]!=''):
            HTtzdifference=(int(teamtimezoneinfo[item[6]])-int(item[14]))
            if HTtzdifference<0:
                HTwest=str(abs(HTtzdifference))
                HTeast='0'
            else:
                HTeast=str(HTtzdifference)
                HTwest='0'
        else:
            HTeast='NULL'
            HTwest='NULL'
        if (item[6] in teamtimezoneinfo.keys())and(item[1] in teamtimezoneinfo.keys()):
            singleentry=item[:6]+[ATeast,ATwest,'','','',teamconferenceinfo[item[1]]]+item[6:11]+[HTeast,HTwest,'','','',teamconferenceinfo[item[6]]]+item[11:15]+item[-1:]+[str(int(item[10])-int(item[5]))]
        elif (item[6] in teamtimezoneinfo.keys()):
            singleentry=item[:6]+[ATeast,ATwest,'','','','NULL']+item[6:11]+[HTeast,HTwest,'','','',teamconferenceinfo[item[6]]]+item[11:15]+item[-1:]+[str(int(item[10])-int(item[5]))]
        elif (item[1] in teamtimezoneinfo.keys()):
            singleentry=item[:6]+[ATeast,ATwest,'','','',teamconferenceinfo[item[1]]]+item[6:11]+[HTeast,HTwest,'','','','NULL']+item[11:15]+item[-1:]+[str(int(item[10])-int(item[5]))]
        else:
            singleentry=item[:6]+[ATeast,ATwest,'','','','NULL']+item[6:11]+[HTeast,HTwest,'','','','NULL']+item[11:15]+item[-1:]+[str(int(item[10])-int(item[5]))]
        appendix=[]
        homecourtinfo=['','','','']
        if (singleentry[11] in conferencebids.keys())and(singleentry[22] in conferencebids.keys()):
            appendix.append(str(conferencebids[singleentry[22]]-conferencebids[singleentry[11]]))
            homecourtinfo.append(str(conferencebids[singleentry[11]]))
            homecourtinfo.append(str(conferencebids[singleentry[22]]))
        else:
            appendix.append('NULL')
            homecourtinfo.append('NULL')
            homecourtinfo.append('NULL')
        if (singleentry[12] in teamconferenceinfo.keys())and(singleentry[1] in teamconferenceinfo.keys()):
            if teamconferenceinfo[singleentry[12]]==teamconferenceinfo[singleentry[1]]:
                appendix.append('1')
            else:
                appendix.append('0')
        else:
            appendix.append('NULL')
        if (('Conference Tourney' in singleentry[27])or('Conference Tournament' in singleentry[27])or('Conference To' in singleentry[27])or('Big Ten Tourney' in singleentry[27]))and(singleentry[27]!=''):
            appendix.append('1')
            appendix.append('0')
        elif (singleentry[27]!=''): 
            appendix.append('0')
            appendix.append('1')
        else:
            if appendix[1]!='NULL':
                appendix.append('0')
                appendix.append('0')
            else:
                appendix.append('NULL')
                appendix.append('NULL')
        if singleentry[12] in teamstadiuminfo.keys():
            if teamstadiuminfo[singleentry[12]] in singleentry[23]:
                appendix.append('1')
            else:
                appendix.append('0')
        else:
            appendix.append('NULL')
        # Secondary Homecourt, Neutral Game, Equidistance, Close to Away, Around State
        # All of them are based on the distance input so it cannot be done in this program
        # Exclude the tournament Game
        teamentry=[]
        for teamindex in range(len(teamname)):
            if (teamname[teamindex]==singleentry[1])and(appendix[-1]=='1'):
                teamentry.append('-1')
            elif (teamname[teamindex]==singleentry[12])and(appendix[-1]=='1'):
                teamentry.append('1')
            else:
                teamentry.append('0')
        total.append(singleentry+appendix+homecourtinfo+teamentry)
    lastindex=0
    secondhomecourt={}
    for item in total:
        if lastindex!=0:
            lastindex=lastindex+1
            if (item[33]=='1')or(item[32]=='1')or(item[31]=='1'):
                item[34]='0'
            elif (item[33]=='NULL'):
                item[34]='NULL'
            else:
                if not(item[12] in secondhomecourt.keys()):
                    secondhomecourt[item[12]]={}
                    secondhomecourt[item[12]][item[23]]=1
                else:
                    if not(item[23] in secondhomecourt[item[12]].keys()):
                        secondhomecourt[item[12]][item[23]]=1
                        #print(secondhomecourt[item[12]])
                    else:
                        secondhomecourt[item[12]][item[23]]=secondhomecourt[item[12]][item[23]]+1;
        else:
            lastindex=lastindex+1
    lastindex=0
    for item in total:
        if lastindex!=0:
            lastindex=lastindex+1
            try:
                if secondhomecourt[item[12]][item[23]]>=3:
                    item[34]='1'
                    print(item[12],item[23],secondhomecourt[item[12]][item[23]],item[34])
                else:
                    item[34]='0'
                    print(item[12],item[23],secondhomecourt[item[12]][item[23]],item[34])
            except:
                pass
        else:
            lastindex=lastindex+1    
    fout=open('D:\\Matchinfo\\Finalspreadsheet'+yearshort+'.csv','w',newline='')
    csvWriter=csv.writer(fout,dialect='excel')
    csvWriter.writerows(total)
    fout.close()
    finmatch.close()
    finteam.close()
