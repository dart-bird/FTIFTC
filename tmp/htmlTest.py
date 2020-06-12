import sys
# sys.stdout = open('output.txt','w',encoding="utf8")
# file = open('test.txt', 'r',encoding="utf8")  
# name = file.read()
from bs4 import BeautifulSoup
import urllib.request
import requests
import urllib.parse
import random
import json
import time
def loadJson(link):
    nickName = []
    req = requests.get(link)
    return req.json()
def getSummonerKDA(soup):
    gameAverageStatus = soup.find("table",{"class":"GameAverageStats"})
    kda = gameAverageStatus.find("span",{"class":"KDARatio"}).get_text().strip()
    kda = kda[0:kda.find(':')]
    return kda
def getsummonerId(soup):
    try:
        return soup.select('div[data-summoner-id]')[0]['data-summoner-id']
    except Exception as e:
        print(soup)
def getSoloRankedData(mySummonerId):
    jsonData = loadJson("https://www.op.gg/summoner/matches/ajax/averageAndList/startInfo=0&summonerId="+mySummonerId+"&type=soloranked")
    soup =  BeautifulSoup(jsonData["html"], "html.parser")
    return soup
print(getSummonerKDA(getSoloRankedData("84690431")))
# targetStr1 = "\\\"".replace("\"","")+"t"
# targetStr2 = "\\\"".replace("\"","")+"n"
# name = name.replace(targetStr1, '').replace(targetStr2,'')
# name = name.replace("><",">\n<")
# print(name)