import requests as rq
import json;
import os;

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/3?view=kona_player_info";

# make request
players = rq.get(url=url, headers = {
    'X-Fantasy-Filter': '{"players":{"filterStatsForExternalIds":{"value":[2023,2024]},"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForSourceIds":{"value":[0,1]},"useFullProjectionTable":{"value":true},"sortAppliedStatTotal":{"sortAsc":false,"sortPriority":3,"value":"102024"},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"PPR"},"sortPercOwned":{"sortPriority":4,"sortAsc":false},"limit":0,"filterRanksForSlotIds":{"value":[0,2,4,6,17,16,8,9,10,12,13,24,11,14,15]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002024","102024","002023","022024"]}}}'
})

# convert to indented json
players_str = json.dumps(players.json(), indent = 4);

#write to json file
with open(os.path.join(os.path.dirname(__file__), './json/players.json'), 'w') as f:
    f.write(players_str);