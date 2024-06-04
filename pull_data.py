import pandas
import os

from espn_data_pull import pull_espn_data
from nfl_data_pull import pull_nfl_data
from fp_data_pull import pull_fp_data

pwd = os.getcwd()

# pull the data into dataframes
espn_df = pull_espn_data()
fp_df = pull_fp_data()
nfl_df = pull_nfl_data()

espn_df.to_csv(os.path.join(pwd, "csv_data", "espn.csv"), index=False)
fp_df.to_csv(os.path.join(pwd, "csv_data", "fp.csv"), index=False)
nfl_df.to_csv(os.path.join(pwd, "csv_data", "nfl.csv"), index=False)