#scrapes all nfl fantasy projections from fantasy.nfl.com and places into data frame

#imports
from bs4 import BeautifulSoup
import requests as rq
import copy
import os
import pandas as pd
import json

def pull_espn_data(path) -> None:
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/3?scoringPeriodId=0&view=kona_player_info"
    headers = {
        #"Accept": "application/json",
        #"Accept-Encoding": "gzip, deflate, br",
        "X-Fantasy-Filter": '{"players":{"filterStatsForExternalIds":{"value":[2023,2024]},"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForSourceIds":{"value":[0,1]},"useFullProjectionTable":{"value":true},"sortAppliedStatTotal":{"sortAsc":false,"sortPriority":3,"value":"102024"},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"PPR"},"sortPercOwned":{"sortPriority":4,"sortAsc":false},"limit":0,"filterRanksForSlotIds":{"value":[0,2,4,6,17,16,8,9,10,12,13,24,11,14,15]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002024","102024","002023","022024"]}}}',
        #"Connection": "keep-alive",
        #"Cookie": 'espn-prev-page=fantasy%3Afootball%3Aleague%3Atoolsprojections; _chartbeat4=t=Cm7UIsBE-ByBCmz3lzDbNSdKnmWqE&E=21&x=374&c=28.76&y=11857&w=171; s_c24=1720040117803; s_c24_s=First%20Visit; s_sq=wdgespcom%252Cwdgespge%3D%2526pid%253Dfantasy%25253Afootball%25253Aleague%25253Atoolsprojections%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Ffantasy.espn.com%25252Ffootball%25252Fplayers%25252Fprojections%252523%2526ot%253DA; 33acrossIdFp=GDsgycUYetHhiluRMQMR7JAYsIWlwTIlif%2FcXSA2jb%2FmFEcPCZ58W4%2BLiB9nvSXvNKuqUMf%2FJH6DRZu7wMtDhw%3D%3D; _au_1d=AU1D-0100-001720038403-1A3ZFJ5E-J6S2; _cc_id=808a62347ef34fb36514950490b036fd; _ga=GA1.2.1393132124.1720038403; _gid=GA1.2.423505329.1720038403; _pubcid=9708302a-9996-41ef-8b8d-efe1a8ff771c; _pubcid_cst=zix7LPQsHA%3D%3D; panoramaId_expiry=1720124802532; __eoi=ID=190da8857fa2e048:T=1720037865:RT=1720038400:S=AA-AfjbM7h3_LhD-otG3_9qwkZ8P; __gads=ID=1d3ae01b7672bde3:T=1720037865:RT=1720038400:S=ALNI_MakNLU5sq9exLllgdi2N9_2Gdfk5w; __gpi=UID=00000e63c3e51c95:T=1720037865:RT=1720038400:S=ALNI_MYYurjFa4LIUUnD4TWfPYJ1-1JzHA; cto_bundle=eSY54l9GRTZVSDZxbSUyRmI1U21EZEpQYTlQM3ZhYXlwNSUyQnFwZEI2RnVlSVRsNllVV2h2WUolMkZ3Tm1Od0MxdTk4WjZ1YTdGRGZuWiUyRnZ2cnIlMkJoTUtmRUhmanZ4bHFYQUZWODdteUtZOUFOaWslMkZvd0hOa3FLJTJCR0RINnh1Q0lTcjdVODBrMHp1; AMCVS_EE0201AC512D2BE80A490D4C%40AdobeOrg=1; AMCV_EE0201AC512D2BE80A490D4C%40AdobeOrg=-330454231%7CMCIDTS%7C19908%7CMCMID%7C57217070274144689411756106386886536658%7CMCAID%7CNONE%7CMCOPTOUT-1720045599s%7CNONE%7CMCAAMLH-1720643199%7C7%7CMCAAMB-1720643199%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C3.1.2; IR_9070=1720038399876%7C0%7C1720038399876%7C%7C; _cb=Dp-5tTDtHmvGBCbysM; _cb_svref=https%3A%2F%2Fwww.google.com%2F; _chartbeat2=.1720037868966.1720038399249.1.EwDIOCrMqpgCROLD8DfTgipDOa54a.2; s_c6=1720038399913-New; s_cc=true; s_ecid=MCMID%7C57217070274144689411756106386886536658; s_gpv_pn=fantasy%3Afootball%3Aleague%3Atoolsprojections; s_ensNR=1720038399408-New; _sharedid=370d84ec-e10c-4d0b-a846-1d04fde9da34; _sharedid_cst=zix7LPQsHA%3D%3D; AMCVS_5BFD123F5245AECB0A490D45%40AdobeOrg=1; AMCV_5BFD123F5245AECB0A490D45%40AdobeOrg=-1506532908%7CMCIDTS%7C19908%7CMCMID%7C65733285339910211511642811205136929418%7CMCAAMLH-1720642669%7C7%7CMCAAMB-1720642669%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1720045069s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; _fbp=fb.1.1720037869027.544367155505008104; IR_gbd=espn.com; block.check=false%7Cfalse; check=true; _gcl_au=1.1.1045397340.1720037866; tveAuth=; tveMVPDAuth=; country=ca; hashedIp=6ce4afe184a043e092e865bb81bb308af3ec4c998c8d115839a1c1b66f8bf235; mbox=session#1781a923053e4a75a7befb2114124530#1720039726|PC#1781a923053e4a75a7befb2114124530.34_0#1783282666; userZip=k1s%205b6; SWID=96002C60-175A-4478-C454-9E46ABC2F215',
        #"X-Fantasy-Platform": "kona-PROD-99130feb5897e7bab43529cea10896997b7fbe07",
        #"X-Fantasy-Source": "kona",
    }
    page = rq.get(url = url, headers = headers)
    content = page.json();
    with open(os.path.join(path, "espn_raw.json"), "w") as f:
        json.dump(content, f, indent=4)