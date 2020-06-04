from bs4 import BeautifulSoup
import urllib.request
import requests
import urllib.parse
import random
import json
import sys
sys.stdout = open('result.txt','w',encoding="utf8")
targetLink = "https://www.op.gg/summoner/userName="
myNickName = urllib.parse.quote("10101010010110")
bronzeIds = ['32410244', '67020736', '30441390', '9176703', '8326115', '4576887', '63390171', '5062518', '84243662', '40640413', '84690431', '9914447', '9344511', '45180433', '84411911', '30730226', '1408106', '35391569', '20570251', '1320831', '61010639', '18481745', '82919000', '7290615', '2443804', '84192465', '32731545', '22975760', '5263398', '77340505', 
'11851398', '10589797', '84889307', '23715218', '38960501', '7394705', '83621793', '2832831', '18911749', '8680734', '72540257', '29232188', '41911620', '1469466', '83528750', '22591161', '1192536', '58460936', '22955529', '27890492', '2415919', '8263701', '30421775', '14043615', '14045156', '8391550', '83043346', '49780781', '20240826', '84555749', '40591134', '3929596', '1525544', '20880355', '10689627', '5190153', '73020700', '62501612', '1175733', '2389173', '3442177', '35870531', '32021836', '23851905', '31151223', '44921185', '84667142', 
'20721919', '48121066', '30683537', '83865767', '30040814', '4441722', '8378115', '83856530', '24090607', '83355394', '18113110', '74130158', '21790173', '4926191', '67960542', '65370729', '71960278', '65661544', '46301012', '1721608', '26542874', '82747535', '8911433', '20841026', '2487285', '65931072', '66223101', '35342043', '80110365', '83028861', '84764465', '11171154', '22054469', '4144172', '34140818', '10689131', '79020827', '30773064', '59090792', '30351367', '1637811', '82500839', '21030165', '56371234', '63280166', '18991466', '1095686', '22320156', '53141026', '84334644', '83959524', '11106843', '84638622', '39631627', '41960612', '5002646', '31924436', '82909168', '59980258', '3336605', '11341497', '19461574', '10599974', '21240901', '9633446', '83247789', '84905150', '83812364', '85223618', '11815522', '29781854', '3613018', '3903536', '2488876', '9059680', '72570858', '82858189', '17713498', '1488060', '84142362', '50761664', '2774838', '31824558', '6922860', '83790980', '10059678', '5773659', '2341646', '33421763', '84991522', '81970723', '84952088', '11920796', '6101618', '13732417', '31470125', '17835920', '4291626', '84718848', '6550394']
# def clickDetail():
def dupelremove(list_):
    return list(set(list_))
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
def getGameData(soup):
    gameResults = []
    gameChamps = []
    boxList = soup.findAll("div",{"class":"GameItemWrap"})
    for gameItemWrap in boxList:
        gameResult = gameItemWrap.find("div",{"class":"GameResult"})
        gameResult = gameResult.get_text().strip()
        if gameResult == "Victory":
            gameResults.append(1)
        elif gameResult == "Defeat":
            gameResults.append(0)
        twoTeamChamps = gameItemWrap.find("div",{"class":"FollowPlayers"}).findAll("div",{"class":"__sprite"})
        tmp = []
        for champ in twoTeamChamps:
            tmp.append(champ.get_text())
        tmp = list(set(tmp))
        gameChamps.append(tmp)
    return [gameResults, gameChamps]
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
if __name__ == "__main__":
    gameData = [[],[]]
    # # getting my soloranked data
    # mySummonerId = getsummonerId(loadPage(targetLink+myNickName))
    # soup = getSoloRankedData(mySummonerId)
    # gameData = [getGameData(soup)]
    # summonerNames = collectSummonerName(soup)
    # summonerIds = getsummonerIds(summonerNames)
    # print(summonerIds)
    # print("협곡에서 사는 브론즈 아이디 갯수 : "+str(len(summonerIds)) +"개")
    cnt = 0
    for bronzeId in bronzeIds:
        print("Processing ID: "+ bronzeId)
        
        soup = getSoloRankedData(bronzeId)
        tmp = getGameData(soup)
        gameData[0].append(tmp[0])
        gameData[1].append(tmp[1])
        print(str(cnt+1) + " of "+ str(len(bronzeIds)) +" Completed")
        cnt+=1
    print(len(gameData))
    # gameData = dupelremove(gameData)
    print(len(gameData))
    print(gameData)