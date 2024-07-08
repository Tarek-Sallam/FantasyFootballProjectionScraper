import pandas as pd
import os
import json

def clean_espn_data(rawpath, path) -> None:
    with open(os.path.join(rawpath, "espn_raw.json")) as f:
        content = json.load(f)

    players = content["players"]
    firstNames = [player["player"]["firstName"] for player in players]
    lastNames = [player["player"]["lastName"] for player in players]
    displayNames = [player["player"]["fullName"] for player in players]
    firstNames = [name.replace('III', '').replace('II', '').replace('JR.', '').replace('SR.', '').replace(" V", '').replace('É', 'E').strip().replace(' ', '').replace('-', '').upper() for name in firstNames]
    lastNames = [name.replace('III', '').replace('II', '').replace('JR.', '').replace('SR.', '').replace(" V", '').replace('É', 'E').strip().replace(' ', '').replace('-', '').upper() for name in lastNames]
    names = [firstName+lastName for firstName, lastName in zip(firstNames, lastNames)]
    #stats = [player["player"]["stats"] for player in players]
    pts = [player["player"]["stats"][len(player["player"]["stats"])-1].get("appliedTotal", 0) for player in players]
    
    #for i in range(len(stats)):
       #if ("appliedTotal" not in (stats[i][len(stats[i]) - 1].keys())):
           #print(players[i]["player"]["fullName"])
    
    positionIds = [player["player"]["defaultPositionId"] for player in players]
    positions = []
    for pos in positionIds:
        if pos == 1:
            positions.append("QB")
        elif pos == 2:
            positions.append("RB")
        elif pos == 3:
            positions.append("WR")
        elif pos == 4:
            positions.append("TE")
        elif pos == 5:
            positions.append("K")
        elif pos == 16:
            positions.append("DEF")
    
    data = pd.DataFrame({'name': names, 'last_name': lastNames, 'first_name': firstNames, 'display': displayNames, 'position': positions, "proj": pts})
    data.to_csv(os.path.join(path, "espn.csv"), index=False)

