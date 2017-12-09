# After you run the Everyday Run.py, please check the error of the spreadsheet
# generated "YYYY-MM-DD.source.csv". Make sure this csv file is error free.
# Then you can run this program.

import csv
from math import *
from tkinter import *
from operator import *
class finalspreadsheetcompiler:

# =========================================================================================================================== 
    def check(self):
        try:
            filepath=self.sv.get()
            print(filepath)
            finin=open(filepath,'r')
            tempst=filepath[-21:-11]
            self.datearray=tempst.split('-')
            csvReaderin=csv.reader(finin)
            singlematchinfo=[]
            for item in csvReaderin:
                singlematchinfo.append(item)
        except:
            messagebox.showwarning("Error","Please enter the correct path and filename.")
            return
        try:
            fin=open('C:\\Users\\Administrator\\Dropbox\\Data\\Common\\2014\\2014 with courtinfo.csv','r')##I changed 'Administer to my equivalent location in my path
            csvReadert=csv.reader(fin)
            self.matchinfo=[]
            for item in csvReadert:
                if item != []:
                    self.matchinfo.append(item)
            if self.matchinfo == []:
                for item in singlematchinfo:
                    self.matchinfo.append(item)
                self.textbool.set('No')
                self.svs.set(self.datearray[1]+'/'+self.datearray[2]+'/'+self.datearray[0])
            else:
                counter=0
                for item in self.matchinfo[1:]:
                    st=item[0]
                    datearray=st.split('/')
                    if int(datearray[2])>int(self.datearray[0]):
                        break
                    elif int(datearray[0])>int(self.datearray[1]):
                        break
                    elif int(datearray[1])>int(self.datearray[2]):
                        break
                    else:
                        if [int(datearray[2]),int(datearray[0]),int(datearray[1])]==[int(self.datearray[0]),int(self.datearray[1]),int(self.datearray[2])]:
                            self.textbool.set('Yes')
                            return
                        else:
                            counter=counter+1;
                self.matchinfo=self.matchinfo[:counter+1]+singlematchinfo[1:]+self.matchinfo[counter+1:len(self.matchinfo)]
                self.textbool.set('No')
                self.svs.set(self.datearray[1]+'/'+self.datearray[2]+'/'+self.datearray[0])
        except:
            messagebox.showwarning("Error","Error.")
            return

    def consolidate(self):
        fout=open("C:\\Users\\Administrator\\Dropbox\\Data\\Common\\2014\\"+"2014 with courtinfo.csv","w",newline="")##I changed Administer to the equivalent location in my path
        csvWriter=csv.writer(fout,dialect="excel")
        csvWriter.writerows(self.matchinfo)
        fout.close()

# =========================================================================================================================== 
# Create a GUI for the compiler

    def __init__(self):
        self.win=Tk()
        self.win.title("GaTech NCAA Basketball Research - Data Compiler")
        self.pathlab=Label(text="Path:")
        self.sv=StringVar()
        self.pathent=Entry(textvariable=self.sv)
        self.pathlab.grid(row=0,column=0,sticky=EW)
        self.pathent.grid(row=0,column=1,columnspan=3,sticky=EW)
        self.checkbut=Button(text="Already in the dataset?",command=self.check)
        self.checkbut.grid(row=1,column=0,columnspan=2,sticky=EW)
        self.textbool=StringVar()
        self.checkent=Entry(textvariable=self.textbool)
        self.checkent.grid(row=1,column=2,columnspan=2,sticky=EW)
        self.startdatelab=Label(text="Date(MM/DD/YYYY):")
        self.startdatelab.grid(row=2,column=0)
        self.svs=StringVar()
        self.startdateent=Entry(textvariable=self.svs)
        self.startdateent.grid(row=2,column=1,columnspan=2)
        self.consolidatebut=Button(text="Append",command=self.consolidate)
        self.consolidatebut.grid(row=2,column=3)

a=finalspreadsheetcompiler()
