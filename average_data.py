import pandas as pd
import numpy as np
import os

def find_proj(row: object, df: pd.DataFrame) -> object:
    return (df[df['name'] == row["name"]]['proj'].item())
    
# load csvs
espn = pd.read_csv(os.path.join(os.getcwd(), "csv_data", "espn.csv"))
nfl = pd.read_csv(os.path.join(os.getcwd(), "csv_data", "nfl.csv"))

# get all the rows that the names are not in the other dataset
not_in_nfl = espn.loc[~espn["name"].isin(nfl["name"])].reset_index(drop=True)
not_in_espn = nfl.loc[~nfl["name"].isin(espn["name"])].reset_index(drop=True)

non_zero_nfl = not_in_nfl[not_in_nfl['proj'] != 0].reset_index(drop=True)
non_zero_espn = not_in_espn[not_in_espn['proj'] != 0].reset_index(drop=True)

print("Players not in the ESPN data but in NFL data (need to add to ESPN data): ")
print(non_zero_espn[['first_name', 'last_name', 'proj']])
print("Players not in NFL data but in ESPN data (can remove from ESPN data): ")
print(non_zero_nfl[['first_name', 'last_name', 'proj']])

print("Before removing extra players in ESPN: ")
print(espn)
# remove the espn players that aren't in the NFL dataset
espn = espn.loc[~(espn['name'].isin(not_in_nfl['name']))].reset_index(drop=True)
print("After removing extra players in ESPN: ")
print(espn)

not_in_espn = not_in_espn.assign(proj = 0)
espn = pd.concat([espn, not_in_espn], ignore_index=True).reset_index(drop=True)
print("After adding the extra NFL players into ESPN dataset: ")
espn = espn.drop_duplicates(subset=['name'])
data = nfl
data['proj'] = nfl.apply(lambda x: ((find_proj(x, espn)) + x.proj) / 2, axis=1)
data = data.sort_values(by=['proj'], ascending=False).reset_index(drop=True)
print("Weighted Data: ")
print(data)
data.to_csv(os.path.join(os.getcwd(), 'weighted_data', 'weighted_data.csv'), index=False)

