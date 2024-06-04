import requests as rq
import pandas as pd

def pull_espn_data() -> pd.DataFrame:
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/3?view=kona_player_info";
    headers = {
            'X-Fantasy-Filter': '{"players":{"filterStatsForExternalIds":{"value":[2023,2024]},"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForSourceIds":{"value":[0,1]},"useFullProjectionTable":{"value":true},"sortAppliedStatTotal":{"sortAsc":false,"sortPriority":3,"value":"102024"},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"PPR"},"sortPercOwned":{"sortPriority":4,"sortAsc":false},"limit":0,"filterRanksForSlotIds":{"value":[0,2,4,6,17,16,8,9,10,12,13,24,11,14,15]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002024","102024","002023","022024"]}}}'
    }
    names = []
    pos = []
    pts = []

    players = rq.get(url=url, headers = headers)
    players_list = players.json()["players"];
    names = [item["player"]["fullName"] for item in players_list]

    for player in [item["player"]["defaultPositionId"] for item in players_list]:
        if player == 2:
            pos.append('RB')
        elif player == 3:
            pos.append('WR')
        elif player == 4:
            pos.append('TE')
        elif player == 1:
            pos.append('QB')
        elif player == 5:
            pos.append('K')
        elif player == 16:
            names[len(pos)] = names[len(pos)].split()[0]
            pos.append('DEF')

    #grab the projected point data
    for player in [item["player"]["stats"] for item in players_list]:
        if (len(player) == 2):
            pts.append(player[1]["appliedTotal"])
        else:
            pts.append(player[2]["appliedTotal"])

    
    return(pd.DataFrame({"name": names, "position": pos, "proj": pts}))