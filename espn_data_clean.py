import pandas as pd
import os
import json

def clean_espn_data() -> pd.DataFrame:
    with open(os.path.join(os.getcwd(), "raw_data", "espn.json")) as f:
        content = json.load(f)

    players = content["players"]
    firstNames = [player["player"]["firstName"] for player in players]
    lastNames = [player["player"]["lastName"] for player in players]
    firstNames = [name.replace('III', '').replace('II', '').replace('JR.', '').replace('SR.', '').replace(" V", '').replace('É', 'E').strip().replace(' ', '') for name in firstNames]
    lastNames = [name.replace('III', '').replace('II', '').replace('JR.', '').replace('SR.', '').replace(" V", '').replace('É', 'E').strip().replace(' ', '') for name in lastNames]
    names = [firstName+lastName for firstName, lastName in zip(firstNames, lastNames)]
    positionIds = [player["defaultPositionId"] for player in players]
    positions = []
    for pos in positionIds:
        if pos == 1:
            positions.append("QB")
        elif pos == 2:
            positions.append("RB")
            
