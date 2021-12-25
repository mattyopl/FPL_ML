import requests
import json
import pandas as pd

#initializing variables and data structures

teamDict = {1: "ARS", 2: "AVL", 3: "BRE", 4: "BRI", 5: "BUR", 6: "CHE", 7: "CRY", 8: "EVE", 9: "LEE", 10: "LEI", 11: "LIV", 12: "MCI", 13: "MUN", 14: "NEW", 15: "NOR", 16: "SOU", 17: "TOT", 18: "WAT", 19: "WHU", 20: "WOL"}
positionDict = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}

playerColumns = ["Index", "ID", "Name", "Game Name", "Team", "Position", "Current Price"]
seasonDataColumns = ["Index", "Season Points", "Season Minutes", "Season I", "Season C", "Season T", "Season Bonus", "Season Bonus Points", "Season Beginning Price", "Season End Price", "Season Goals", "Season Assists", "Season YC", "Season RC", "Season Saves", "Season Penalty Saves", "Season OG", "Season Penalty Misses", "Season CS", "Season GC"]

df = pd.DataFrame(columns=playerColumns)

general_data_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
general_data_response = requests.get(general_data_URL)
general_data = json.loads(general_data_response.text)

player_data_URL = "https://fantasy.premierleague.com/api/element-summary/"

ind = 0

#pulling all players' data

for player in general_data["elements"]:

    #general data
    ind = ind + 1
    ID = player["id"]
    Name = player["first_name"] + " " + player["second_name"]
    GameName = player["web_name"]
    Team = teamDict[player["team"]]
    Position = positionDict[player["element_type"]]
    CurrentPrice = (player["now_cost"] - player["cost_change_start"])/10
    generalDF = pd.DataFrame([[ind,ID,Name,GameName,Team,Position,CurrentPrice]], columns=playerColumns)
    
    #pulling individual player data
    URL = player_data_URL + str(ID) + "/"
    response = requests.get(URL)
    data = json.loads(response.text)

    #pulling past season data
    for season in data["history_past"]:
        seasonDataColumns = ["Index", season["season_name"] + " " +  "Season Points", season["season_name"] + " " +  "Season Minutes",season["season_name"] + " " +  "Season I",season["season_name"] + " " +  "Season C",season["season_name"] + " " +  "Season T",season["season_name"] + " " +  "Season Bonus",season["season_name"] + " " +  "Season Bonus Points",season["season_name"] + " " +  "Season Beginning Price",season["season_name"] + " " +  "Season End Price",season["season_name"] + " " +  "Season Goals",season["season_name"] + " " +  "Season Assists",season["season_name"] + " " +  "Season YC",season["season_name"] + " " +  "Season RC",season["season_name"] + " " +  "Season Saves",season["season_name"] + " " +  "Season Penalty Saves",season["season_name"] + " " +  "Season OG",season["season_name"] + " " +  "Season Penalty Misses",season["season_name"] + " " +  "Season CS",season["season_name"] + " " +  "Season GC"]
        Points = season["total_points"]
        Minutes = season["minutes"]
        Inf = season["influence"]
        Crea = season["creativity"]
        Thre = season["threat"]
        Bonus = season["bps"]
        BonusPoints = season["bonus"]
        BeginPrice = season["start_cost"]/10
        EndPrice = season["end_cost"]/10
        Goals = season["goals_scored"]
        Assists = season["assists"]
        YelC = season["yellow_cards"]
        RedC = season["red_cards"]
        Saves = season["saves"]
        PenSaves = season["penalties_saved"]
        OwnGoals = season["own_goals"]
        PenMiss = season["penalties_missed"]
        CleanSheets = season["clean_sheets"]
        GoalsConceded = season["goals_conceded"]
        
        #combine individual player data
        seasonDF = pd.DataFrame([[ind, Points, Minutes, Inf, Crea, Thre, Bonus, BonusPoints, BeginPrice, EndPrice, Goals, Assists, YelC, RedC, Saves, PenSaves, OwnGoals, PenMiss, CleanSheets, GoalsConceded]], columns=seasonDataColumns)
        generalDF = pd.merge(generalDF, seasonDF, how="left")
        

    #combining individual player data to all player dataframe
    df = pd.concat([df, generalDF], sort = False)
    print(GameName)

#yay we have everything
df.to_excel("FPL_Player_Data_Season.xlsx")