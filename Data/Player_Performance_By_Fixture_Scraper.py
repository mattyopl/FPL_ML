import requests
import json
import pandas as pd
from playwright.sync_api import sync_playwright
import time
import datetime
from io import StringIO
import numpy
import os

#Data wanted: Match Data with Elo, Home/Not Home, Scoreline, xG Scoreline since 2014/2015 of Premier League Data

#Initializing

clubEloName = {"West Bromwich Albion": "West Brom","Manchester United":"Man United", "Manchester City":"Man City", "Newcastle United": "Newcastle", "Queens Park Rangers":"QPR","Wolverhampton Wanderers":"Wolves"}

matchColumns = ["Home?", "Elo", "Opponent Elo", "Elo Diff", "Goals Scored", "Goals Conceded", "xG", "xGC"]

#Scraper going through every match in one season of EPL soccer

def matchData(season):
    leagueURL = "https://understat.com/league/EPL/" + str(season)
    seasonDF = pd.DataFrame(columns=matchColumns)

    

    #loop through every team in the league
    for i in range(1,21):
        #initializing browser window
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        #go to the league url for the season
        page.goto(leagueURL)
        #click to the team page for that season
        page.locator("//html/body/div[1]/div[3]/div[3]/div/div[2]/div/table/tbody/tr["+str(i)+"]/td[2]/a").click()

        #get teamname
        teamName = page.locator("//html/body/div[1]/div[3]/ul/li[3]").inner_text()
        if teamName in clubEloName:
            eloName = clubEloName[teamName]
        else:
            eloName = teamName

        urlTeamName = ""
        for letter in teamName:
            if letter == " ":
                urlTeamName = urlTeamName + "_"
            else:
                urlTeamName = urlTeamName + letter
        
        #checking if data already exists
        if str(teamName+str(season)+".xlsx") in os.listdir("C:/Users/matth/OneDrive - Cornell University/Projects/Soccer ML/Fixture Data/"):
            page.close()
            continue
        teamDF = pd.DataFrame(columns=matchColumns)

        #todo:write code to get players eligible
        #loop through every match for the given team
        for j in range(1,39):
            #Understat.com match date pulling
            date = page.locator("//html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[" + str(j) + "]/div[1]").inner_text()

            #Understat.com enemy team name pulling
            opponentTeamName = page.locator("//html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div["+str(j)+"]/div[2]/div/div/a").inner_text()

            if opponentTeamName in clubEloName:
                oppEloName = clubEloName[opponentTeamName]
            else:
                oppEloName = opponentTeamName

            #Changing date formatting
            date = datetime.date.strftime(datetime.datetime.strptime(date, "%b %d, %Y"), "%Y-%m-%d")

            #clubelo elo pulling
            ELO_URL = "http://api.clubelo.com/" + date
            ELO_response = requests.get(ELO_URL)
            ELO_data = StringIO(ELO_response.text)
            ELOs = pd.read_csv(ELO_data, sep=",", nrows=200)
            elo = ELOs.loc[ELOs["Club"]==eloName].iloc[0]["Elo"]
            opponentElo = ELOs.loc[ELOs["Club"]==oppEloName].iloc[0]["Elo"]
            eloDiff = elo - opponentElo

            #navigate to the match page
            page.locator("//html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[" + str(j) + "]/div[2]/div/a").click()

            #determine if it's home or away
            if page.locator("label[for=team-home]").inner_text() == teamName:
                home = True
            else:
                home = False

            #get xG scoreline
            homexg = page.locator("//html/body/div[1]/div[3]/div[4]/div/div[2]/table/tbody[2]/tr/td[9]").inner_text()
            page.locator("//html/body/div[1]/div[3]/div[4]/div/div[1]/div/label[2]").click()
            awayxg = page.locator("//html/body/div[1]/div[3]/div[4]/div/div[2]/table/tbody[2]/tr/td[9]").inner_text()
            if home:
                xG = homexg[0:4]
                xGA = awayxg[0:4]
            else:
                xG = awayxg[0:4]
                xGA = homexg[0:4]

            #get scoreline
            temp = page.locator("//html/body/div[1]/header/div/span").inner_text()
            scoreline = ""
            for i in temp:
                if i not in teamName and i not in opponentTeamName and i != " ":
                    scoreline = scoreline + i
            if home:
                goalsScored = scoreline[0]
                goalsConceded = scoreline[2]
            else:
                goalsScored = scoreline[2]
                goalsConceded = scoreline[0]

            tempDF = pd.DataFrame([[home, elo, opponentElo, eloDiff,goalsScored, goalsConceded, xG, xGA]], columns=matchColumns)
            seasonDF = pd.concat([seasonDF, tempDF])
            teamDF = pd.concat([teamDF, tempDF])
            page.goto("https://understat.com/team/" + urlTeamName + "/" + str(season))
        teamDF.to_excel(teamName + str(season) + ".xlsx")
        page.close()


with sync_playwright() as p:
    matchData(2016)

#unfinished

# seasonColumns = []
# tempColumns = []
# for k in range(1,39):
#     seasonColumns.append("Season 2019-2020 GW" + str(k))
#     tempColumns.append("Season 2020-2021 GW" + str(k))


# dfColumns = numpy.concatenate((seasonColumns,tempColumns))

# df = pd.read_excel("Data_Mastersheet.xlsx")

# #Find players who are eligible for Each Team
# def players(index):
#     eligiblePlayers = []
#     teamname =teamDict1[index]
#     for i in range(len(df["Team"])):
#         if df["Team"][i] == teamname:
#             eligiblePlayers.append(df["Game Name"][i])
#         elif len(eligiblePlayers)!=0:
#             i = len(df["Team"])
#     return eligiblePlayers

# teamDict1 = {1: "ARS", 2: "AVL", 3: "BRE", 4: "BRI", 5: "BUR", 6: "CHE", 7: "CRY", 8: "EVE", 9: "LEE", 10: "LEI", 11: "LIV", 12: "MCI", 13: "MUN", 14: "NEW", 15: "NOR", 16: "SOU", 17: "TOT", 18: "WAT", 19: "WHU", 20: "WOL"}
# teamDict = {1:"Arsenal", 2:"Aston_Villa", 3: "Brentford", 4:"Brighton", 5:"Burnley", 6:"Chelsea", 7:"Crystal_Palace", 8:"Everton", 9:"Leeds", 10:"Leicester", 11:"Liverpool", 12:"Manchester_City", 13:"Manchester_United", 14:"Newcastle_United", 15:"Norwich", 16:"Southampton", 17:"Tottenham", 18:"Watford", 19:"West_Ham", 20:"Wolverhampton_Wanderers"}