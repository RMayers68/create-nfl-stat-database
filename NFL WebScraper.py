"""
Intended purpose of program is to scrape the data from a football statistic website to place in a database for future use
Richard Mayers July 10th, 2023
"""


from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

NFL_TEAMS = {
    0: 'Arizona Cardinals',
    1: 'Atlanta Falcons',
    2: 'Baltimore Ravens',
    3: 'Buffalo Bills',
    4: 'Carolina Panthers',
    5: 'Chicago Bears',
    6: 'Cincinnati Bengals',
    7: 'Cleveland Browns',
    8: 'Dallas Cowboys',
    9: 'Denver Broncos',
    10: 'Detroit Lions',
    11: 'Green Bay Packers',
    12: 'Houston Texans',
    13: 'Indianapolis Colts',
    14: 'Jacksonville Jaguars',
    15: 'Kansas City Chiefs',
    16: 'Las Vegas Raiders',
    17: 'Los Angeles Chargers',
    18: 'Los Angeles Rams',
    19: 'Miami Dolphins',
    20: 'Minnesota Vikings',
    21: 'New England Patriots',
    22: 'New Orleans Saints',
    23: 'New York Giants',
    24: 'New York Jets',
    25: 'Philadelphia Eagles',
    26: 'Pittsburgh Steelers',
    27: 'San Francisco 49ers',
    28: 'Seattle Seahawks',
    29: 'Tampa Bay Buccaneers',
    30: 'Tennessee Titans',
    31: 'Washington Football Team'
}

#function to pull data from {year} {teams} webpage
def data_pull(teamID,year):
    #variable creation
    weeks = []
    opponent = []
    teamScore = []
    oppTeamScore = []
    
    #BeautifulSoup used to turn URL info into easily readable information
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dataRowCount = []
    for x in range (24):
        dataRowCount.append(x)
        
    #finding the trs that have the data we want
    games = soup.find('table',{'id':'games'})
    games_div = games.find_all('tr',{'data-row':dataRowCount})
    dataRowCount.clear()
    
    loopNum = 0
    #for loop to run through every game
    for container in games_div:
        if(str(container.find('th',{'data-stat':'week_num'})) is None):
            break
        else:
            weeks.append(loopNum)
            textOpponent = container.find('td',{'data-stat':'opp'}).text.strip()
            opponent.append(textOpponent)
            teamScore.append(container.find('td',{'data-stat':'pts_off'}).text.strip())
            oppTeamScore.append(container.find('td',{'data-stat':'pts_def'}).text.strip())           
            loopNum += 1
        
    for week in weeks:
        if (opponent[week] == "" or opponent[week] == "Bye Week"):
            print(str(f" {year} Week {week+1}: {NFL_TEAMS[teamID]} Bye Week")) 
        else:
            print(str(f" {year} Week {week+1}: {NFL_TEAMS[teamID]} - {opponent[week]} {teamScore[week]}-{oppTeamScore[week]}.")) 
            
            
#team name constants
TEAMS = ["crd","atl","rav","buf","car","chi","cin","cle","dal","den","det","gnb",
         "htx","clt","jax","kan","rai","sdg","ram","mia","min","nwe","nor","nyg",
         "nyj", "phi","pit","sfo","sea","tam","oti","was"]


#create driver object with fast page loading strategy
options = Options()
options.page_load_strategy = 'none'
driver = webdriver.Chrome(options=options)

# causes data pulled to be in English
headers = {"Accept-Language": "en-US, en;q=0.5"}

# URL's informations stored in seperate variable
for team in range(0,32):
    for year in reversed(range(1970,2023)):
        url = f"https://www.pro-football-reference.com/teams/{TEAMS[team]}/{year}.htm"
        try:
            driver.get(url)
            time.sleep(1)
            data_pull(team,year)            
        except AttributeError:
            print(f"{NFL_TEAMS[team]} did not play in {year}.")
            time.sleep(3)
            
driver.quit()



