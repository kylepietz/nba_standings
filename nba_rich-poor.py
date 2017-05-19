from bs4 import BeautifulSoup
import urllib.request
import html5lib
#import pandas as pd
#import time
import statistics
from matplotlib import pyplot as plt

D = {}

def getRecords(year):
    url = \
        "http://www.landofbasketball.com/yearbyyear/" + str(year) + "_" + str(year+1) + "_standings.htm"

    req = urllib.request.Request(url, headers={'User-Agent': 'Safari/10.1'})
    soup = BeautifulSoup(urllib.request.urlopen(req).read(), "html5lib")


    #print(soup.find_all('div', 'rd-100-50'))
    winsPerTeam = []
    lossesPerTeam = []

    if year <= 1970:
        standings = soup.find_all('tr')
    else:
        standings = soup.find_all('tr')[:2]
    
    for row in soup.find_all('tr'):
        if len(row) >= 7:
            #print(row.contents[5].text)
            if row.contents[5].text != 'W':
                winsPerTeam += [int(row.contents[5].text)]
            if row.contents[7].text != 'L':
                lossesPerTeam += [int(row.contents[7].text)]

    totalGames = winsPerTeam[0] + lossesPerTeam[0]               
    totalTeams = len(winsPerTeam)
    if year == 1954:
        #taking away exceptional case
        totalTeams -= 1
        winsPerTeam = winsPerTeam[:-1]
        lossesPerTeam = lossesPerTeam[:-1]
        

    D[year] = (winsPerTeam, lossesPerTeam, totalGames, totalTeams)

difList = []
for y in range(1946,2017):
    getRecords(y)
    dif = statistics.stdev(D[y][0])/D[y][2]
    difList += [dif]

plt.plot(range(1946,2017),difList)
plt.xlabel('Year')
plt.ylabel('Win Gap')
plt.title('Rich/Poor Gap throughout NBA History')
plt.show()



