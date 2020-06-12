from bs4 import BeautifulSoup
import urllib.request
import requests
import urllib.parse
import random
import json
import time
# import sys
import pandas as pd
# sys.stdout = open('result.txt','w',encoding="utf8")
targetLink = "https://www.op.gg/summoner/userName="
myNickName = urllib.parse.quote("10101010010110")
# def clickDetail():
def dupelremove(input_list):
    input_dic = {}
    r_list = []
    for i, v in enumerate(input_list):
        get_value = input_dic.get(v, None)
        if get_value == None:
            input_dic[v] = i
            r_list.append(v)
    return r_list
def summonerNameQuote(summonerName):
    return urllib.parse.quote(summonerName)
def loadPage(link):
    nickName = []
    req = urllib.request.urlopen(url=link)
    data = req.read()
    soup = BeautifulSoup(data, "html.parser")
    return soup
def loadJson(link):
    nickName = []
    req = requests.get(link)
    return req.json()
def collectSummonerName(soup):
    summonerNames = []
    boxList = soup.findAll("div",{"class":"GameItemList"})
    for game in boxList:
        currentTeam = game.findAll("div",{"class":"Summoner"})
        for target_list in currentTeam:
            # print(target_list)
            summonerNames.append(target_list.find("a").get_text().strip())
    summonerNames = dupelremove(summonerNames)
    return summonerNames
def getSummonerKDA(soup):
    gameAverageStatus = soup.find("table",{"class":"GameAverageStats"})
    kda = gameAverageStatus.find("span",{"class":"KDARatio"}).get_text().strip()
    kda = kda[0:kda.find(':')]
    return kda
def getGameData(soup):
    gameData = []
    boxList = soup.findAll("div",{"class":"GameItemWrap"})
    cnt = 0
    for gameItemWrap in boxList:
        print("getting gameResult & KDA ..." + str(cnt) + " of 20 complete.")
        tmp = []
        tmpName = []
        isOneTeam = False
        gameResult = gameItemWrap.find("div",{"class":"GameResult"})
        gameResult = gameResult.get_text().strip()
        teams = gameItemWrap.find("div",{"class":"FollowPlayers"}).findAll("div",{"class","Team"})
        oneTeamNames = teams[0]
        twoTeamNames = teams[1]
        if gameResult != "Remake":
            if gameResult == "Victory":
                tmp.append(1)
            else:
                tmp.append(0)
            for i in range(0,5):
                    if "Requester" in oneTeamNames.select('div[class]')[i*5]['class']:
                        isOneTeam = True
            if isOneTeam == True:
                for name in oneTeamNames.findAll("div",{"class":"Summoner"}):
                    tmpName.append(name.find("a",{"class":"Link"}).get_text())
            else:
                for name in twoTeamNames.findAll("div",{"class":"Summoner"}):
                    tmpName.append(name.find("a",{"class":"Link"}).get_text())
            for tmpName_ in tmpName:
                print("get KDA from ... <"+tmpName_+"> Summoner")
                tmpSummonerId = getsummonerId(loadPage(targetLink+urllib.parse.quote(tmpName_)))
                soup = getSoloRankedData(tmpSummonerId)
                tmp.append(getSummonerKDA(soup))
            gameData.append(tmp)
        cnt += 1
    print(gameData)
    return gameData
def getsummonerId(soup):
    return soup.select('div[data-summoner-id]')[0]['data-summoner-id']
def getsummonerIds(summonerNames):
    summonerIds = []
    for summonerName in summonerNames:
        
        soup = loadPage(targetLink+urllib.parse.quote(summonerName))
        Id = getsummonerId(soup)
        print("SummonerId : "+Id)
        summonerIds.append(Id)
        print(str(len(summonerIds))+ " of "+str(len(summonerNames))+" Collected")
    return summonerIds
def getDataGameIds(soup):
    return [div['data-game-id'] for div in soup.select('div[data-game-id]')]
def getSoloRankedData(mySummonerId):
    jsonData = loadJson("https://www.op.gg/summoner/matches/ajax/averageAndList/startInfo=0&summonerId="+mySummonerId+"&type=soloranked")
    soup = BeautifulSoup(jsonData["html"], "html.parser")
    return soup
def moreData(summonerIds, summonerNames):
    soup = getSoloRankedData(summonerIds[random.randint(0,len(summonerIds)-1)])
    tmpSummonerNames = collectSummonerName(soup)
    summonerNames = summonerNames + tmpSummonerNames
    summonerNamesOut = dupelremove(summonerNames)
    tmpSummonerIds = getsummonerIds(tmpSummonerNames)
    summonerIds = summonerIds + tmpSummonerIds
    summonerIdsOut =  dupelremove(summonerIds)
    return [summonerNamesOut, summonerIdsOut]
if __name__ == "__main__":
    gameData = [[],[]]
    # # getting nicknames in my soloranked data
    mySummonerId = getsummonerId(loadPage(targetLink+myNickName))
    soup = getSoloRankedData(mySummonerId)
    summonerNames = collectSummonerName(soup)
    summonerIds = getsummonerIds(summonerNames)
    # more collect Ids
    tmpData = moreData(summonerIds, summonerNames)
    summonerNames = tmpData[0]
    summonerIds = tmpData[1]

    tmpData = moreData(summonerIds, summonerNames)
    summonerNames = tmpData[0]
    summonerIds = tmpData[1]

    tmpData = moreData(summonerIds, summonerNames)
    summonerNames = tmpData[0]
    summonerIds = tmpData[1]
    print(summonerIds)
    print("현재까지 모은 협곡에서 사는 아이디 갯수 : " + str(len(summonerIds)) +"개")
    ## 아래 코드는 챔피언 상성을 따져 승패 정보를 기록하는 코드
    ## 하지만 라벨링 너무 많아서 drop
    # cnt = 0
    # df = pd.DataFrame(columns=['gameResult', 'oChamp1', 'oChamp2', 'oChamp3', 'oChamp4', 'oChamp5'])
    # for bronzeId in summonerIds:
    #     print("Processing ID: "+ bronzeId)
    #     soup = getSoloRankedData(bronzeId)
    #     tmp = getGameData(soup)
    #     tmp_df = pd.DataFrame(columns=['gameResult', 'oChamp1', 'oChamp2', 'oChamp3', 'oChamp4', 'oChamp5'], data=tmp)
    #     df = pd.concat([df,tmp_df],join="outer",ignore_index=True)
    #     print(str(cnt+1) + " of "+ str(len(summonerIds)) +" Completed")
    #     cnt+=1
    # # df.drop(['Unnamed: 0'],axis=1,inplace=True)
    # df.to_csv('sample_more2Bronze.csv')