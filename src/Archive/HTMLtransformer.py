import csv
from re import findall
from tkinter import *
from operator import *

class htmldatatransformer:
    
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

    def matchtimezone(self):
        Virgintime=['Virgin Islands','Puerto Rico']
        Easterntime=['Bahamas','ME','NH','MA','VT','RI','CT','NJ','PA','DE','DC','MD','VA','WV','OH','MI','IN','NC','SC','GA','FL','NY']
        Mountaintime=['MT','WY','CO','NM','ID','UT','AZ']
        Pacifictime=['WA','OR','CA','NV']
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
        else:
            self.thisgameinfo.append('')
        if (self.thisgameinfo[-3]=='Lexington')and(self.thisgameinfo[-2]=='KY'):
            self.thisgameinfo[-1]=0
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
            
    def strip(self):
        fin=open(self.address,"r")
        aday=fin.read()
        fin.close()
        teamnames=findall("</td><td  align=left class=yspscores><b>(.+)</span>&nbsp;</td></tr>",aday)
        courtnames=findall("<td height=20 class=yspscores>(.*)<br>",aday)
        self.gameinfo=[['','Away Team','AT 1st Half Score','AT 2nd Half Score','AT OT Score','AT Total Score','Home Team','HT 1st Half Score','HT 2nd Half Score','HT OT Score','HT Total Score','Home Court','City','State','Timezone']]
        aa=list(range(0,len(teamnames),2))
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
                self.thisgameinfo=[self.datest]
                self.thisgameinfo=self.thisgameinfo+nameaway+pointsaway+namehome+pointshome
                self.thisgameinfo.append(courtnames[int(i/2)])
                #print(self.thisgameinfo)
                self.parenthesissep()
                self.matchtimezone()
                self.gameinfo.append(self.thisgameinfo)
                self.totalgameinfo.append(self.thisgameinfo)

    def output(self):
        fout=open(self.address[:-4]+".csv","w",newline="")
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(self.gameinfo)
        fout.close()
  
        
    def transform(self):
        self.folderpath=self.sv.get()
        self.startdatest=self.svs.get()
        self.enddatest=self.sve.get()
        self.startdatearray=self.startdatest.split('/')
        self.enddatearray=self.enddatest.split('/')
        self.totalgameinfo=[['','Away Team','AT 1st Half Score','AT 2nd Half Score','AT OT Score','AT Total Score','Home Team','HT 1st Half Score','HT 2nd Half Score','HT OT Score','HT Total Score','Home Court','City','State','Timezone']]
        for i in range(3):
            self.startdatearray[i]=int(self.startdatearray[i])
            self.enddatearray[i]=int(self.enddatearray[i])
        self.datearray=self.startdatearray
        while (self.datearray!=self.enddatearray):
            try:
                self.datest=str(self.datearray[2])+'-'+str(self.datearray[0])+'-'+str(self.datearray[1])
                self.address=self.folderpath+self.datest+'.source.html'
                self.strip()
                self.output()
                if mod(self.datearray[2],4)==0:
                    self.month=self.leapmonth
                else:
                    self.month=self.regmonth
                self.datearray[1]=self.datearray[1]+1
                if self.datearray[1]>self.month[self.datearray[0]]:
                    self.datearray[1]=1
                    self.datearray[0]=self.datearray[0]+1
                if self.datearray[0]>12:
                    self.datearray[2]=self.datearray[2]+1
                    self.datearray[0]=1
            except:
                #pass
                messagebox.showerror("Error","Please enter a valid path and valid dates")
                raise ValueError
        fout=open("D:\\Matchinfo\\"+self.folderpath[-5:-1]+" with courtinfo.csv","w",newline="")
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(self.totalgameinfo)
        fout.close()

    def __init__(self):
        self.regmonth=[0,31,28,31,30,31,30,31,31,30,31,30,31]
        self.leapmonth=[0,31,29,31,30,31,30,31,31,30,31,30,31]
        self.win=Tk()
        self.win.title("GaTech NCAA Basketball Research - Data Transformer")
        self.pathlab=Label(text="Path:")
        self.sv=StringVar()
        self.pathent=Entry(textvariable=self.sv)
        self.transbut=Button(text="Transform Data",command=self.transform)
        self.pathlab.grid(row=0,column=0,sticky=EW)
        self.pathent.grid(row=0,column=1,columnspan=3,sticky=EW)
        self.startdatelab=Label(text="Start Date(MM/DD/YYYY):")
        self.svs=StringVar()
        self.startdateent=Entry(textvariable=self.svs)
        self.enddatelab=Label(text="End Date(MM/DD/YYYY):")
        self.sve=StringVar()
        self.enddateent=Entry(textvariable=self.sve)
        self.startdatelab.grid(row=1,column=0)
        self.startdateent.grid(row=1,column=1)
        self.enddatelab.grid(row=1,column=2)
        self.enddateent.grid(row=1,column=3)
        self.transbut.grid(row=2,column=0,columnspan=4,sticky=EW)
        self.win.mainloop()

a=htmldatatransformer()
