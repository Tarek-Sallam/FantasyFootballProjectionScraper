#scrapes all nfl fantasy projections from fantasy pros and places into data frame

#imports
from bs4 import BeautifulSoup
import requests
import pandas as pd

def pull_fp_data() -> pd.DataFrame:
    # part 1 of the url (need to concatenate offset to get all players)
    urlpt1 = "https://www.fantasypros.com/nfl/projections/"
    urlpt2 = ".php?week=draft"
    pos_list = ["rb", "qb", "wr", "dst", "td", "k"]

    # lists to fill with data
    names = []
    pts = []
    pos = []


    for current_pos in pos_list:
        url = urlpt1 + current_pos + urlpt2
            # get the page and parse it
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features="html.parser")

        # find the table and find the table body
        table = soup.find('table')
        table_body = table.find('tbody')
            
        # get the name elements, point elements and position elements
        players_els = table_body.find_all('tr')
        pts_els = []
        names_els = []

        for player_el in players_els:
            pts_els.append(player_el.find_all("td")[-1])
            names_els.append(player_el.find('a'))
            if (current_pos == 'dst'):
                pos.append('DEF')
            else:
                pos.append(current_pos.upper())
            
        #strip the names and points and positions
        names.extend([name.text for name in names_els])
        pts.extend([pts.text for pts in pts_els])

    #return a dataframe with the data
    return pd.DataFrame({'name': names, 'position': pos, 'proj': pts})

pull_fp_data()