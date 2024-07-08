import pandas as pd
import os
import json

def clean_nfl_data(rawpath, path) -> None:
    players = pd.read_csv(os.path.join(rawpath, "nfl_raw.csv"))
    display = players["name"].to_list()
    pos = players["position"].to_list()
    pts = players["proj"].to_list()
    lastNames = [name.split()[-1].replace('III', '').replace('II', '').replace('JR.', '').replace('SR.', '').replace(" V", '').replace('É', 'E').strip().replace(' ', '').replace('-', '').upper() for name in display]
    firstNames = [(''.join(name.split().pop())).replace('III', '').replace('II', '').replace('JR.', '').replace('SR.', '').replace(" V", '').replace('É', 'E').strip().replace(' ', '').replace('-', '').upper() for name in display]
    names = [firstName+lastName for firstName, lastName in zip(firstNames, lastNames)]
    data = pd.DataFrame({'name': names, 'last_name': lastNames, 'first_name': firstNames, 'display': display, 'position': pos, 'proj': pts})
    data.to_csv(os.path.join(path, "nfl.csv"), index=False)

