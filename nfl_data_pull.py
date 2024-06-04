#scrapes all nfl fantasy projections from fantasy.nfl.com and places into data frame

#imports
from bs4 import BeautifulSoup
import requests
import pandas as pd

def pull_nfl_data() -> pd.DataFrame:
    # part 1 of the url (need to concatenate offset to get all players)
    urlpt1 = "https://fantasy.nfl.com/research/projections?offset="

    # part 2 of the url
    urlpt2 = "&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2024&statType=seasonProjectedStats&statWeek=1"

    # lists to fill with data
    names = []
    pts = []
    pos = []

    # loop through the amount of pages
    for i in range(38):

        # concatenate the urls with the offset 
        url = urlpt1 + str(i * 25 + 1) + urlpt2
        # get the page and parse it
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features="html.parser")

        # find the table and find the table body
        table = soup.find('table')
        table_body = table.find('tbody')
        
        # get the name elements, point elements and position elements
        names_els = table_body.find_all('a', class_ = 'playerName')
        pos_els = table_body.find_all('em')
        pts_els = table_body.find_all('td', class_ = 'projected')
        
        # strip the names and points and positions
        names.extend([name.text for name in names_els])
        pts.extend([pts.text for pts in pts_els])
        pos.extend([pos.text.split()[0] for pos in pos_els])

    # return a dataframe with the data
    return pd.DataFrame({'name': names, 'position': pos, 'proj': pts})
pull_nfl_data()