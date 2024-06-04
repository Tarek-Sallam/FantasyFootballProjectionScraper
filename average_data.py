import pandas as pd
import os

espn = pd.read_csv(os.path.join(os.getcwd(), "csv_data", "espn.csv"))
fp = pd.read_csv(os.path.join(os.getcwd(), "csv_data", "fp.csv"))
nfl = pd.read_csv(os.path.join(os.getcwd(), "csv_data", "nfl.csv"))

print(nfl)