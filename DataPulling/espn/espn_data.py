import requests as rq
import json;

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/players?scoringPeriodId=0&view=players_wl";

r = rq.get(url=url, headers={
    'Accept': 'application/json', 
    'Accept-Encoding': 'gzip, deflate, br', 
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'X-Fantasy-Filter': '{"filterActive":{"value":true}}',
    'X-Fantasy-Platform': 'kona-PROD-aa413c7e338f6f98dbe8ea58e2d60e26ef8e3949',
    'X-Fantasy-Source': 'kona'
    });
#print(json.dumps(dict(r.headers), indent = 4));
str = json.dumps(r.json(), indent = 4);
with open("raw/players.json", 'w') as f:
    f.write(str);