import pandas as pd
import numpy as np
import os

# load csvs
espn = pd.read_csv(os.path.join(os.getcwd(), "csv_data", "espn.csv"))
nfl = pd.read_csv(os.path.join(os.getcwd(), "csv_data", "nfl.csv"))

# get all the rows that the names are not in the other dataset
not_in_espn = nfl.loc[~((nfl["last_name"].isin(espn["last_name"])) & (nfl["first_name"].isin(espn["first_name"])))]
not_in_nfl = espn.loc[~((espn["last_name"].isin(nfl["last_name"])) & (espn["first_name"].isin(nfl["first_name"])))]

# remove all names that aren't in the nfl dataset from the espn dataset (since we can't draft them anyways)
espn2 = espn.loc[~(espn["last_name"].isin(not_in_nfl["last_name"]) & (espn["first_name"].isin(not_in_nfl["first_name"])))];

# set all the names that aren't in the espn dataset to 0
not_in_espn["proj"] = not_in_espn["proj"].apply(lambda x: 0.0)

# add all the names that aren't in the espn dataset to the espn dataset
espn2 = pd.concat([espn2, not_in_espn])