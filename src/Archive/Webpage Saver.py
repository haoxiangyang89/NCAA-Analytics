import urllib.request

for month in range(1,4):
    for date in range(1,32):
        address="http://rivals.yahoo.com/ncaa/basketball/scoreboard?d="+"2013-"+str(month)+"-"+str(date)
        webFile=urllib.request.urlopen(address)
        localFile=open("D:\\2013\\2013\\"+"2013-"+str(month)+"-"+str(date)+".source.html","wb")
        st=webFile.read()
        #print(st[500:1000])
        localFile.write(st)
        webFile.close()
        localFile.close()
