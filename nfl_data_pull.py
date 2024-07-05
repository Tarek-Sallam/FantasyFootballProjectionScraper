#scrapes all nfl fantasy projections from fantasy.nfl.com and places into data frame

#imports
from bs4 import BeautifulSoup
import requests
import os
import copy
import pandas as pd
import json

def pull_nfl_data() -> None:
    # part 1 of the url (need to concatenate offset to get all players)
    urlpt1 = "https://fantasy.nfl.com/research/projections?offset="

    # part 2 of the url
    urlpt2 = "&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2024&statType=seasonProjectedStats&statWeek=1"

    # lists to fill with data
    names = []
    lastNames = []
    display = []
    pts = []
    pos = []
    combined = []

    # loop through the amount of pages for offense
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
        display.extend([name.text for name in names_els])
        pts.extend([float(pts.text) for pts in pts_els])
        pos.extend([pos.text.split()[0] for pos in pos_els])


    # pull the kickers data (same process as above)
    urlpt1 = "https://fantasy.nfl.com/research/projections?offset="
    urlpt2 = "&position=7&sort=projectedPts&statCategory=projectedStats&statSeason=2024&statType=seasonProjectedStats"
    
    for j in range(2):
        url = urlpt1 + str(j * 25 + 1) + urlpt2
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features="html.parser")

        table = soup.find('table')
        table_body = table.find('tbody')
        
        # get the name elements, point elements and position elements
        names_els = table_body.find_all('a', class_ = 'playerName')
        pos_els = table_body.find_all('em')
        pts_els = table_body.find_all('td', class_ = 'projected')
        
        display.extend([name.text for name in names_els])
        pts.extend([float(pts.text) for pts in pts_els])
        pos.extend([pos.text.split()[0] for pos in pos_els])

    urlpt1 = "https://fantasy.nfl.com/research/projections?offset="
    urlpt2 = "&position=8&sort=projectedPts&statCategory=projectedStats&statSeason=2024&statType=seasonProjectedStats"

    #copy display names to name list
    names = copy.deepcopy(display)
    # pull the defense data (same process as above)
    for k in range(2):
        url = urlpt1 + str(k * 25 + 1) + urlpt2
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features="html.parser")
        table = soup.find('table')
        table_body = table.find('tbody')
        
        # get the name elements, point elements and position elements
        names_els = table_body.find_all('a', class_ = 'playerName')
        pos_els = table_body.find_all('em')
        pts_els = table_body.find_all('td', class_ = 'projected')
        
        display.extend([name.text for name in names_els])
        names.extend([name.text.split()[-1] for name in names_els])
        pts.extend([float(pts.text) for pts in pts_els])
        pos.extend([pos.text.split()[0] for pos in pos_els])

    
    names[:] = [name.upper().replace('III', '').replace('II', '').replace('JR.', '').replace('SR.', '').replace(" V", '').replace('É', 'E').strip() for name in names]
    lastNames = copy.deepcopy(names)
    firstNames = copy.deepcopy(names)
    firstNames[:] = [firstName.split(' ', 1)[0].replace(' ', '') for firstName in firstNames]
    lastNames[:] = [lastName.split(' ', 1)[-1].replace(' ', '') for lastName in lastNames]
    combined[:] = [name.replace(' ', '') for name in names]

    # return a dataframe with the data
    data = pd.DataFrame({"name": combined, "last_name": lastNames, 'first_name': firstNames,'display': display,'position': pos, 'proj': pts})
    data.to_csv(os.path.join(os.getcwd(), "csv_data", "nfl.csv"), index=False)
