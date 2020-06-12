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
myNickName = urllib.parse.quote("영원히잊을수없는")


Ids = ['71750378', '18681419', '4460427', '84597287', '51730382', '84278253', '57671404', '54692988', '29341663', '84597223', '60811200', '25260179', '3458580', '3263292', '16910609', '2187036', '84480645', '84578910', '82626310', '84473360', '84706526', '84473350', '22876013', '83625123', '80640535', '65821228', '27971322', '26691029', '83459580', '84477997', '84488849', '28552004', '43920725', '58390689', '84473233', '84477123', '22611767', '43120962', '83043017', '84474011', '16020164', '83635062', '84599317', '81261978', '85106850', '56921556', '50970876', '76100166', '47600290', '23606470', '83873584', '84590645', '54811204', '47820563', '47780258', '84597591', '82571497', '76860185', '84477111', '61080452', '76191002', '84471039', '83486872', '83399133', '84473303', '82539100', '9100379', '82545997', '84516821', '84473617', '84473423', '22825024', '72130732', '17615858', '84473624', '8201453', '73800331', '71020652', '73451014', '50730879', '55131776', '84620363', '73540668', '83511119', '84470845', '83460107', '30430942', '2712005', '35010825', '85086957', '83955845', '82700263', '83455258', '76990129', '46510279', '54743978', '65721509', '42095093', '22071749', '40261890', '83624221', '3253276', '66301571', '55110801', '84844766', '17556449', '11943987', '43871730', '84471392', '66031564', '84614942', '83156756', '18101239', '34181252', '84471777', '61050186', '83971073', '36990696', '52133166', '65841156', '28742441', '83579483', '16810685', '82922688', '9707124', '84486051', '54724682', '1971751', '43850443', '56561224', '83893807', '80862522', '62380878', '54804802', '84314387', '11800783', '53900234', '84473056', '84473241', '77320905', '51651113', '84473246', '83448554', '41721324', '84487443', '83455733', '84475423', '84471343', '9891629', '20622163', '83955959', '1103553', '82842252', '69170643', '84490264', '85105684', '77070143', '23692628', '84287708', '65640959', '3480396', '2545410', '84202620', '8726073', '84516822', '76860288', '84665624', '84147029', '54864166', '59360473', '3149868', '83411792', '41780625', '83473110', '2481136', '50840809', '18320216', '24910546', '84473672', '8342164', '82681611', '1225219', '35950866', 
'35441832', '84478103', '84709226', '84473359', '83675895', '84473279', '31212721', '50260171', '83043018', '20850261', '4260918', '17571984', '45641407', '38680194', '84000590', '84469482', '33682291', '25301734', '54904131', '84475067', '84473298', '33451337', '84474411', '84490266', '79330941', '66090406', '84477761', '3730692', '80371199', '67770716', '42022952', '84488710', '84473287', '25170222', '76130297', '77310760', '83783950', '66750357', '83505377', '67750294', '36711775', '67730405', '11706234', '71070809', '1990503', '63071145', '7480670', '77030235', '84472961', '18941663', '26610151', '85306396', '51780290', '75770400', '48830223', '82588856', '84717833', '38120473', '70550137', '60790916', '83465757', '76910765', '83102266', '13762462', '66323838', '22972574', '84055408', '51520727', '83959133', '45370748', '38941060', '84480646', '4843289', '45631469', '84471362', '77070169', '73770459', '57541180', '26421732', '83214063', '84583674', '10502958', '85023347', '31551938', '26670323', '29341237', '28920777', '17574071', '38371270', '13965344', '77180222', '13684896', '46311009', '50751123', '79280308', '78510653', '55860385', '22861513', '41780873', '84018875', '84765789', '17564611', '83628440', '8865750', '83604103', '80370646', '60320841', '60291596', '38552629', '67240658', '84293743', '48040865', '84471551', '22191421', '82913579', '83752310', '79760155', '19421492', '51060360', '83278863', '81250450', '1222794', '77860708', '85295826', '77200702', '84503485', '41935288', '83587108', '9999050', '83713434', '84477992', '2395962', '66090153', '20450514', '75780469', '48031052', '1215275', '57321585', '84725977', '84680752', '74750173']

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

