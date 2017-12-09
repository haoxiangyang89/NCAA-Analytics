% This will be a long project. Let's start here.
% QUEST analysis for NCAA Basketball bracket prediction

% Updated 3/24/2014 using the logistic regression probability as the values
% to update the Quest.

function [avgq] = NCAAQuest(alpha,beta,year)

    function [nameObj] = loadName(year)
        [ndata,text1,alldata1] = xlsread('C:\Documents\ISYE\Research\Massey Data\Teams names and numbers New.xlsx');
        nameset = alldata1(:,(year-2000)*2+2);
        nameset = nameset(3:length(nameset));
        numberset = alldata1(:,(year-2000)*2+1);
        numberset = numberset(3:length(numberset));
        nameset(cellfun(@(nameset) any(isnan(nameset)),nameset)) = [];
        numberset(cellfun(@(numberset) any(isnan(numberset)),numberset)) = [];
        nameObj = containers.Map(nameset,numberset);
    end

nameObj=loadName(year);                                                              %load the names and the numbers
yrstr=num2str(year);
[number,text,alldata] = xlsread(['C:\Documents\ISYE\Research\Massey Data\Massey',yrstr,'.csv']);

    function [y] = yconverter(x,alpha,beta)
        % convert a certain x into y
        y=exp(alpha*x+beta)/(1+exp(alpha*x+beta));
    end

    function [x] = xconverter(y,alpha,beta)
        % convert a certain y into x
        if y>1
            y=0.9999999;
        elseif y<0
            y=0.0000001;
        else
            y=y;
        end
        temp1=log(y/(1-y));
        temp2=temp1-beta;
        x=(temp2)/alpha;
    end

% Construct all 348 team's profile
for i=[1:length(nameObj)]
    yy=yconverter(0,alpha,beta);
    q(i)=QuestCreate(yy,0.1,0.796,3.5,0.01,0,0.01,2);
end

for i=[2:length(alldata)]
    atname = cell2mat(alldata(i,5));  % Away/Home team name
    atscore = cell2mat(alldata(i,6)); % Away/Home team score
    atnumber = nameObj(atname);       % Away/Home team number
    
    htname = cell2mat(alldata(i,2)); 
    htscore = cell2mat(alldata(i,3));
    htnumber = nameObj(htname);
    
    update = htscore - atscore;
    if cell2mat(alldata(i,10))==0
        homecourtAdv = 2;
    else
        homecourtAdv = 0;
    end
    atpup=xconverter(QuestMean(q(atnumber)),alpha,beta);
    htpup=xconverter(QuestMean(q(htnumber)),alpha,beta);
    updateh = yconverter((htscore - atscore - homecourtAdv)+atpup,alpha,beta);
    updatea = yconverter((atscore - htscore + homecourtAdv)+htpup,alpha,beta);
    if update > 0
        q(htnumber)=QuestUpdate(q(htnumber),updateh,0);
        q(atnumber)=QuestUpdate(q(atnumber),updatea,1);
    else
        q(htnumber)=QuestUpdate(q(htnumber),updateh,1);
        q(atnumber)=QuestUpdate(q(atnumber),updatea,0);
    end
    
end

for i=[1:length(nameObj)]
    avgq(i) = QuestMean(q(i));
end
end