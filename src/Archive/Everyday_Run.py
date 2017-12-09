# Please run it every day to save the webpage and generate the spreadsheet

# When you run it, the input should be yesterday's date to make sure we get
# every match of that day

# After generating the spreadsheet, please check with ESPN or Rivals.com to
# to make sure each entry is correct

import urllib.request
import csv
from re import findall
from tkinter import *
from operator import *
class htmldatatransformer:

# ===========================================================================================================================
# Save the webpage in the dropbox. Please make a copy on your laptop too!

# If you dropbox has a different path, please make sure you change it or it
# will throw you an error
    def htmlsaver(self):
        self.folderpath=self.sv.get()
        self.startdatest=self.svs.get()
        self.startdatearray=self.startdatest.split('/')
        year=self.startdatearray[2]
        month=self.startdatearray[0]
        day=self.startdatearray[1]
        address="http://rivals.yahoo.com/ncaa/basketball/scoreboard?d="+year+"-"+month+"-"+day
        webFile=urllib.request.urlopen(address)
        localFile=open(self.folderpath+year+"-"+month+"-"+day+".source.html","wb")
        st=webFile.read()
        localFile.write(st)
        webFile.close()
        localFile.close()
        
# ===========================================================================================================================
#separate city and state information inside the parenthesis

    def parenthesissep(self):
        st=self.thisgameinfo[-1]
        if st!='':
            try:
                #print(st)
                temp1=findall('\((.+)\)',st)
                temp2=temp1[0].split(',')
                city=temp2[0].strip()
                state=temp2[1].strip()
                self.thisgameinfo.append(city)
                self.thisgameinfo.append(state)
            except:
                self.thisgameinfo.append('')
                self.thisgameinfo.append('')
        else:
            self.thisgameinfo.append('')
            self.thisgameinfo.append('')
            
# ===========================================================================================================================
#obtain timezone information of the court
    def matchtimezone(self):
        Germantime=['Germany']
        Virgintime=['Virgin Islands','Puerto Rico','British Virgin Islands']
        Easterntime=['Mexico','Bahamas','ME','NH','MA','VT','RI','CT','NJ','PA','DE','DC','MD','VA','WV','OH','MI','IN','NC','SC','GA','FL','NY']
        Mountaintime=['MT','WY','CO','NM','ID','UT','AZ']
        Pacifictime=['WA','OR','CA','NV','BC']
        Centraltime=['ND','SD','MN','WI','IA','NE','KS','MO','IL','KY','TN','AL','AR','MS','LA','OK','TX']
        Hawaiitime=['HI']
        Altime=['AK']
        if self.thisgameinfo[-1] in Easterntime:
            self.thisgameinfo.append('0')
        elif self.thisgameinfo[-1] in Centraltime:
            self.thisgameinfo.append('1')
        elif self.thisgameinfo[-1] in Mountaintime:
            self.thisgameinfo.append('2')
        elif self.thisgameinfo[-1] in Pacifictime:
            self.thisgameinfo.append('3')
        elif self.thisgameinfo[-1] in Hawaiitime:
            self.thisgameinfo.append('5')
        elif self.thisgameinfo[-1] in Altime:
            self.thisgameinfo.append('4')
        elif self.thisgameinfo[-1] in Virgintime:
            self.thisgameinfo.append('-1')
        elif self.thisgameinfo[-1] in Germantime:
            self.thisgameinfo.append('-6')
        else:
            self.thisgameinfo.append('')
        if (self.thisgameinfo[-3]=='Lexington')and(self.thisgameinfo[-2]=='KY'):
            self.thisgameinfo[-1]=0
        if (self.thisgameinfo[-3]=='Puerto Vallarta')and(self.thisgameinfo[-2]=='Mexico'):
            self.thisgameinfo[-1]=1
        if (self.thisgameinfo[-3]=='Louisville')and(self.thisgameinfo[-2]=='KY'):
            self.thisgameinfo[-1]=0
        if (self.thisgameinfo[-3]=='Morehead')and(self.thisgameinfo[-2]=='KY'):
            self.thisgameinfo[-1]=0
        if (self.thisgameinfo[-3]=='Richmond')and(self.thisgameinfo[-2]=='KY'):
            self.thisgameinfo[-1]=0
        if (self.thisgameinfo[-3]=='Chattanooga')and(self.thisgameinfo[-2]=='TN'):
            self.thisgameinfo[-1]=0
        if (self.thisgameinfo[-3]=='Johnson City')and(self.thisgameinfo[-2]=='TN'):
            self.thisgameinfo[-1]=0
        if (self.thisgameinfo[-3]=='Knoxville')and(self.thisgameinfo[-2]=='TN'):
            self.thisgameinfo[-1]=0
        if (self.thisgameinfo[-3]=='Evansville')and(self.thisgameinfo[-2]=='IN'):
            self.thisgameinfo[-1]=1
        if (self.thisgameinfo[-3]=='Oakland City')and(self.thisgameinfo[-2]=='IN'):
            self.thisgameinfo[-1]=1
        if (self.thisgameinfo[-3]=='Valparaiso')and(self.thisgameinfo[-2]=='IN'):
            self.thisgameinfo[-1]=1
        if (self.thisgameinfo[-3]=='Moscow')and(self.thisgameinfo[-2]=='ID'):
            self.thisgameinfo[-1]=3

# ===========================================================================================================================
#use RegEx to extract match and court

    def strip(self):
        fin=open(self.address,"r")
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
                self.datest1=self.startdatearray[0]+'/'+self.startdatearray[1]+'/'+self.startdatearray[2]
                self.thisgameinfo=[self.datest1]
                self.thisgameinfo=self.thisgameinfo+nameaway+pointsaway+namehome+pointshome
                self.thisgameinfo.append(courtnames[int(i/2)])
                self.parenthesissep()
                self.matchtimezone()
                self.gameinfo.append(self.thisgameinfo)
                self.totalgameinfo.append(self.thisgameinfo)

# ===========================================================================================================================
#output

    def output(self):
        fout=open(self.address[:-5]+".csv","w",newline="")
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(self.gameinfo)
        fout.close()

# ===========================================================================================================================  
#read the starting date and the ending date and read the information from html files        
    def transform(self):
        self.folderpath=self.sv.get()
        self.startdatest=self.svs.get()
        self.startdatearray=self.startdatest.split('/')
        self.totalgameinfo=[['','Away Team','AT 1st Half Score','AT 2nd Half Score','AT OT Score','AT Total Score','Home Team','HT 1st Half Score','HT 2nd Half Score','HT OT Score','HT Total Score','Home Court','City','State','Timezone']]
        try:
            self.datest=self.startdatearray[2]+'-'+self.startdatearray[0]+'-'+self.startdatearray[1]
            self.address=self.folderpath+self.datest+'.source.html'
            self.strip()
            self.output()
        except:
            messagebox.showerror("Error","Please enter a valid path and valid dates")
            raise ValueError

# ===========================================================================================================================
# Create a GUI for the entire data input method

    def __init__(self):
        self.regmonth=[0,31,28,31,30,31,30,31,31,30,31,30,31]
        self.leapmonth=[0,31,29,31,30,31,30,31,31,30,31,30,31]
        self.win=Tk()
        self.win.title("GaTech NCAA Basketball Research - Data Transformer")
        self.pathlab=Label(text="Path:")
        self.sv=StringVar()
        self.pathent=Entry(textvariable=self.sv)
        self.savebut=Button(text="Save HTML File",command=self.htmlsaver)
        self.transbut=Button(text="Transform Data",command=self.transform)
        self.pathlab.grid(row=0,column=0,sticky=EW)
        self.pathent.grid(row=0,column=1,columnspan=3,sticky=EW)
        self.startdatelab=Label(text="Date(MM/DD/YYYY):")
        self.svs=StringVar()
        self.startdateent=Entry(textvariable=self.svs)
        self.startdatelab.grid(row=1,column=0,columnspan=2)
        self.startdateent.grid(row=1,column=2,columnspan=2)
        self.savebut.grid(row=2,column=0,columnspan=2,sticky=EW)
        self.transbut.grid(row=2,column=2,columnspan=2,sticky=EW)
        self.win.mainloop()

a=htmldatatransformer()

# ===========================================================================================================================
# The common error in the spreadsheet might be:
# 1. The team name is missing (Yes, it is missing!) because some teams are
#   just not in Yahoo's database
# 2. The match may have other data points missing. Just delete the whole match
#   when you see something like this
# 3. The cancelled/delayed/not yet played match
# 4. Be patient. There might be some other surprising errors.

# Have fun with this!!!
