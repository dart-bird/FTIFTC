from bs4 import BeautifulSoup
import urllib.request
import requests
import urllib.parse
import random
import json
import time
import pandas as pd
import parmap 
import asyncio
from multiprocessing import Manager
from tqdm import tqdm
targetLink = "https://www.op.gg/summoner/userName="
myNickName = urllib.parse.quote("10101010010110")

def loadPage(link):
    req = urllib.request.urlopen(url=link)
    data = req.read()
    soup = BeautifulSoup(data, "html.parser")
    return soup
def loadJson(link):
    nickName = []
    req = requests.get(link)
    return req.json()
def getsummonerId(soup):
    try:
        return soup.select('div[data-summoner-id]')[0]['data-summoner-id']
    except Exception as e:
        print(soup)
def getsummonerIds(summonerNames):
    summonerIds = []
    for summonerName in tqdm(summonerNames,desc='getting summonerIds',smoothing=1.0):
        
        soup = loadPage(targetLink+urllib.parse.quote(summonerName))
        Id = getsummonerId(soup)
        # print("SummonerId : "+Id)
        summonerIds.append(Id)
        # print(str(len(summonerIds))+ " of "+str(len(summonerNames))+" Collected")
    return summonerIds
def getSoloRankedData(mySummonerId):
    jsonData = loadJson("https://www.op.gg/summoner/matches/ajax/averageAndList/startInfo=0&summonerId="+mySummonerId+"&type=soloranked")
    soup =  BeautifulSoup(jsonData["html"], "html.parser")
    return soup
def getGameData(soup):
    gameData = []
    boxList = soup.findAll("div",{"class":"GameItemWrap"})
    cnt = 0
    for gameItemWrap in boxList:
        # print("getting gameResult & KDA ..." + str(cnt) + " of 20 complete.")
        isOneTeam = False
        gameResult = gameItemWrap.find("div",{"class":"GameResult"})
        gameResult = gameResult.get_text().strip()
        teams = gameItemWrap.find("div",{"class":"FollowPlayers"}).findAll("div",{"class","Team"})
        oneTeamNames = teams[0]
        twoTeamNames = teams[1]
        if gameResult != "Remake":
            if gameResult == "Victory":
                gameData.append(1)
            else:
                gameData.append(0)
            for i in range(0,5):
                    if "Requester" in oneTeamNames.select('div[class]')[i*5]['class']:
                        isOneTeam = True
                        break
            if isOneTeam == True:
                for name in oneTeamNames.findAll("div",{"class":"Summoner"}):
                    gameData.append(name.find("a",{"class":"Link"}).get_text())
            else:
                for name in twoTeamNames.findAll("div",{"class":"Summoner"}):
                    gameData.append(name.find("a",{"class":"Link"}).get_text())
        cnt += 1
    # print(gameData)
    return gameData
def getSummonerKDA(soup):
    gameAverageStatus = soup.find("table",{"class":"GameAverageStats"})
    kda = gameAverageStatus.find("span",{"class":"KDARatio"}).get_text().strip()
    kda = kda[0:kda.find(':')]
    return kda
def dupelremove(input_list):
    input_dic = {}
    r_list = []
    for i, v in enumerate(input_list):
        get_value = input_dic.get(v, None)
        if get_value == None:
            input_dic[v] = i
            r_list.append(v)
    return r_list
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
def a(x, d):
    soup = getSoloRankedData(x)
    data = getGameData(soup)
    d.append(data)
def b(i, d):
    i = i - 1
    for j in range(1,6):
        # print(d[i*6+j])
        d[i*6+j] = getsummonerId(loadPage(targetLink+urllib.parse.quote(d[i*6+j])))
        # print(d[i*6+j])
def c(i, d):
    i = i - 1
    for j in range(1,6):
        d[i*6+j] = getSummonerKDA(getSoloRankedData(d[i*6+j]))
if __name__ == "__main__":

    try:
        manager = Manager() 
        oldGameDataList = manager.list()
        gameDataList = manager.list()
        # TODO : 첫 째 닉네임을 모은다.
        mySummonerId = getsummonerId(loadPage(targetLink+myNickName))
        soup = getSoloRankedData(mySummonerId)
        summonerNames = collectSummonerName(soup)
        summonerIds = getsummonerIds(summonerNames)
        # TODO : 둘 째 해당 닉네임에 대한 게임 데이터를 가져온다 .
        # Example > [1,topNick, jungleNick, midNick, botNick, supportNick, 1, topNick, jungleNick, ... ]
        num_cores = 8 # 사용할 cpu 코어 수. multiprocessing.cpu_count() 로 확인 가능 
        
        tqdm(parmap.map(a, summonerIds, oldGameDataList,pm_pbar=True, pm_processes=num_cores),desc='Store gameDataList',smoothing=1.0)

        for i in range(len(oldGameDataList)):
            for j in oldGameDataList[i]:
                gameDataList.append(j)

        # TODO : 셋 째 Nick to Id 작업진행
        tqdm(parmap.map(b, range(1,int(len(gameDataList)/6)-1), gameDataList,pm_pbar=True, pm_processes=num_cores),desc='Nick to Id converting',smoothing=1.0)
        # TODO : 넷 째 게임 데이터 리스트에서 topId -> topId KDA 로 바꾸면서 게임 데이터를 완성시킨다.
        tqdm(parmap.map(c, range(1,int(len(gameDataList)/6)-1), gameDataList,pm_pbar=True, pm_processes=num_cores),desc='Id to KDA converting',smoothing=1.0)
        # TODO : 데이터를 최종적으로 쌓는 작업을 진행한다.
        df = pd.DataFrame(columns=['gameResult', 'TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT'])
        for i in tqdm(range(1,int(len(gameDataList)/6)-1),desc='Saving csv',smoothing=1.0): # 판 수를 계산하고 변환작업
            i = i - 1
            tmp = [[gameDataList[i*6],gameDataList[i*6+1],gameDataList[i*6+2],gameDataList[i*6+3],gameDataList[i*6+4],gameDataList[i*6+5]]]
            tmp_df = pd.DataFrame(columns=['gameResult', 'TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT'], data=tmp)
            df = pd.concat([df,tmp_df],join="outer",ignore_index=True)
        df.to_csv('sample_RenameKDA.csv')
    except Exception as e:
        df = pd.DataFrame(columns=['gameResult', 'TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT'])
        for i in tqdm(range(1,int(len(gameDataList)/6)-1),desc='Saving csv',smoothing=1.0): # 판 수를 계산하고 변환작업
            i = i - 1
            tmp = [[gameDataList[i*6],gameDataList[i*6+1],gameDataList[i*6+2],gameDataList[i*6+3],gameDataList[i*6+4],gameDataList[i*6+5]]]
            tmp_df = pd.DataFrame(columns=['gameResult', 'TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'SUPPORT'], data=tmp)
            df = pd.concat([df,tmp_df],join="outer",ignore_index=True)
        df.to_csv('sample_RenameKDA.csv')
        print(e)

