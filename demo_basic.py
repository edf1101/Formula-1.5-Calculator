'''
This demo shows the basic functionality of the f1point5 library. It simply imports the race / sprint data
for the 2023 season so far and then excludes Red Bull from the race results and recalculates the points
scored by both constructors and drivers
'''

import f1point5 as f1

# A list of all the teams full names below so you can pick and choose which you want to include
all_teams = ['Red Bull Racing Honda RBPT', 'Aston Martin Aramco Mercedes', 'Ferrari', 'Mercedes',
             'Alfa Romeo Ferrari', 'Alpine Renault', 'Williams Mercedes', 'AlphaTauri Honda RBPT',
             'Haas Ferrari', 'McLaren Mercedes']

banned_teams = ['Red Bull Racing Honda RBPT']  # In this example we are only excluding Red Bull

# Race & Sprint data from 2023 up to the Japanese Grand Prix
race_data_address = "data/Formula1_2023season_raceResults.csv"
sprint_data_address = "data/Formula1_2023season_sprintResults.csv"


season_2023 = f1.Season(banned_teams, race_data_address, sprint_data_address) # create the season race & standing data
season_standings = season_2023.getStandings()

# print the seasons driver championship standings so far
print(season_standings.getDriverTable())

