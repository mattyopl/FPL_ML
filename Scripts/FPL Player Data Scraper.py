import requests
import json
import pandas as pd

# initializing variables and data structures

teamDict = {1: "Arsenal", 2: "Aston_Villa", 3: "Bournemouth", 4: "Brentford", 5: "Brighton", 6: "Chelsea", 7: "Crystal_Palace", 8: "Everton", 9: "Fulham", 10: "Leeds",
            11: "Leicester", 12: "Liverpool", 13: "Manchester City", 14: "Manchester United", 15: "Newcastle United", 16: "Nottingham_Forest", 17: "Southampton", 
            18: "Tottenham", 19: "West_Ham", 20: "Wolverhampton_Wanderers"}
positionDict = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}

playerColumns = ["Index", "ID", "Name", "Game Name",
                 "Team", "Position", "Current Price"]
seasonDataColumns = ["Index", "Season Points", "Season Minutes", "Season I", "Season C", "Season T", "Season Bonus", "Season Bonus Points", "Season Beginning Price",
                     "Season End Price", "Season Goals", "Season Assists", "Season YC", "Season RC", "Season Saves", "Season Penalty Saves", "Season OG", "Season Penalty Misses", "Season CS", "Season GC"]

df = pd.DataFrame(columns=playerColumns)

general_data_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
general_data_response = requests.get(general_data_URL)
general_data = json.loads(general_data_response.text)

player_data_URL = "https://fantasy.premierleague.com/api/element-summary/"

ind = 0

# pulling all players' data

for player in general_data["elements"]:

    # general data
    ind = ind + 1
    ID = player["id"]
    Name = player["first_name"] + " " + player["second_name"]
    GameName = player["web_name"]
    Team = teamDict[player["team"]]
    Position = positionDict[player["element_type"]]
    CurrentPrice = (player["now_cost"] - player["cost_change_start"])/10
    generalDF = pd.DataFrame(
        [[ind, ID, Name, GameName, Team, Position, CurrentPrice]], columns=playerColumns)

    # pulling individual player data
    URL = player_data_URL + str(ID) + "/"
    response = requests.get(URL)
    data = json.loads(response.text)

    # pulling past season data
    for season in data["history_past"]:
        seasonDataColumns = ["Index", season["season_name"] + " " + "Season Points", season["season_name"] + " " + "Season Minutes", season["season_name"] + " " + "Season I", season["season_name"] + " " + "Season C", season["season_name"] + " " + "Season T", season["season_name"] + " " + "Season Bonus", season["season_name"] + " " + "Season Bonus Points", season["season_name"] + " " + "Season Beginning Price", season["season_name"] + " " + "Season End Price",
                             season["season_name"] + " " + "Season Goals", season["season_name"] + " " + "Season Assists", season["season_name"] + " " + "Season YC", season["season_name"] + " " + "Season RC", season["season_name"] + " " + "Season Saves", season["season_name"] + " " + "Season Penalty Saves", season["season_name"] + " " + "Season OG", season["season_name"] + " " + "Season Penalty Misses", season["season_name"] + " " + "Season CS", season["season_name"] + " " + "Season GC"]
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

        # combine individual player data
        seasonDF = pd.DataFrame([[ind, Points, Minutes, Inf, Crea, Thre, Bonus, BonusPoints, BeginPrice, EndPrice, Goals,
                                Assists, YelC, RedC, Saves, PenSaves, OwnGoals, PenMiss, CleanSheets, GoalsConceded]], columns=seasonDataColumns)
        generalDF = pd.merge(generalDF, seasonDF, how="left")

    # combining individual player data to all player dataframe
    df = pd.concat([df, generalDF], sort=False)
    print(GameName)

# yay we have everything
df.to_excel("FPL_Player_Data_Season.xlsx")
