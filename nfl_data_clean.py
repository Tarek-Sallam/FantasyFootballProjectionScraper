import pandas as pd
import os
import json

def clean_nfl_data(rawpath, path) -> None:
    players = pd.read_csv(os.path.join(rawpath, "nfl_raw.csv"))
    display = players["name"].to_list()
    pos = players["position"].to_list()
    pts = players["proj"].to_list()
    nameArr = [name.upper().replace('-', '').replace('É', 'E').replace("'", '').strip().split() for name in display]
    prohibitedStrs = ['III', 'II', 'JR.', 'SR.', 'V']
    for i in range(len(nameArr)):
        for chars in nameArr[i]:
            if chars in prohibitedStrs:
                nameArr[i].remove(chars)

    lastNames = [name[-1].upper() for name in nameArr]
    for name in nameArr:
        name.pop()
    firstNames = [''.join(name) for name in nameArr]
    names = [firstName+lastName for firstName, lastName in zip(firstNames, lastNames)]
    for i in range(len(pos)):
        if pos[i] == 'DEF':
            firstNames[i] = lastNames[i]
            names[i] = lastNames[i]
        if firstNames[i] == 'JOSHUA':
            firstNames[i] = 'JOSH'
            names[i] = firstNames[i] + lastNames[i]
        if firstNames[i] == 'CEDRICK':
            firstNames[i] = 'CED'
            names[i] = firstNames[i] + lastNames[i]
        if firstNames[i] == 'MICHAEL':
            firstNames[i] = 'MIKE'
            names[i] = firstNames[i] + lastNames[i]
        
    data = pd.DataFrame({'name': names, 'last_name': lastNames, 'first_name': firstNames, 'display': display, 'position': pos, 'proj': pts})
    data.to_csv(os.path.join(path, "nfl.csv"), index=False)

