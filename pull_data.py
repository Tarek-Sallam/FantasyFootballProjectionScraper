import pandas
import os

from espn_data_pull import pull_espn_data
from nfl_data_pull import pull_nfl_data

# pull the data into dataframes
pull_espn_data()
pull_nfl_data()