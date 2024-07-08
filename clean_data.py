from espn_data_clean import clean_espn_data
from nfl_data_clean import clean_nfl_data

import os

clean_espn_data(os.path.join(os.getcwd(), "raw_data"), os.path.join(os.getcwd(), "csv_data"))
clean_nfl_data(os.path.join(os.getcwd(), "raw_data"), os.path.join(os.getcwd(), "csv_data"))
