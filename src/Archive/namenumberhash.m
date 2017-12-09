% Import the NCAA Teams and Numbers
[ndata,text,alldata] = xlsread('C:\Documents\ISYE\Research\Teams names and numbers.xlsx');
nameset = alldata(:,1);
nameset = nameset(2:349);
numberset = 1:348;
nameObj = containers.Map(nameset,numberset);
save('nameObj.mat','nameObj');