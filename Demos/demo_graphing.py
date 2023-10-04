'''
This demo draws a graph of each driver's points over the course of a season (this data only goes up to
Japan at the time of writing though) It also plots each driver's line with their team colour
'''

# need to import pandas and matplotlib here, so we can work with and plot the data
import f1point5 as f1
import pandas as pd
import matplotlib.pyplot as plt

banned_teams = ['Red Bull Racing Honda RBPT', 'Mercedes', 'Ferrari']  # In this example we excluding top 3 teams

# The team colour of each driver
driver_colors = {'Max Verstappen': (0, 0, 0.4), 'Sergio Perez': (0, 0, 0.4),
                 'Carlos Sainz': (0.9, 0, 0), 'Charles Leclerc': (0.9, 0, 0),
                 'Valtteri Bottas': (0.6, 0, 0), 'Guanyu Zhou': (0.6, 0, 0),
                 'Lewis Hamilton': (0, 0.7, 0.65), 'George Russel': (0, 0.7, 0.65),
                 'Lando Norris': (0.9, 0.5, 0), 'Oscar Piastri': (0.9, 0.5, 0),
                 'Pierre Gasly': (0.3, 0.5, 0.9), 'Esteban Ocon': (0.3, 0.5, 0.9),
                 'Fernando Alonso': (0, 0.3, 0), 'Lance Stroll': (0, 0.3, 0),
                 'Yuki Tsunoda': (0.3, 0.3, 0.3), 'Nyck De Vries': (0.3, 0.3, 0.3),
                 'Daniel Ricciardo': (0.3, 0.3, 0.3), 'Liam Lawson': (0.3, 0.3, 0.3),
                 'Kevin Magnussen': (0.5, 0.5, 0.5), 'Nico Hulkenberg': (0.5, 0.5, 0.5),
                 'Alexander Albon': (0, 0, 0.5), 'Logan Sargeant': (0, 0, 0.5)}

# Race & Sprint data from 2023 up to the Japanese Grand Prix
race_data_address = "data/Formula1_2023season_raceResults.csv"
sprint_data_address = "data/Formula1_2023season_sprintResults.csv"

# create the season race & standing data
season_2023 = f1.Season(banned_teams, race_data_address, sprint_data_address)

# Fetch all drivers and races part of this season
all_drivers = season_2023.getAllDrivers()
all_races = season_2023.getAllRaces()

races_thus_far = []
standings_by_time = None

for race in all_races:  # go through each race in the dataset
    races_thus_far += [race]

    # get the standings up to the race we're currently looking at, but rename points to race name
    current_standings = season_2023.getStandings(races_thus_far).getDriverTable().rename(columns={'Points': race})

    # if this is first race seen then make new standings by time dataframe else add this dataframe onto the end of it
    if len(races_thus_far) == 1:
        standings_by_time = current_standings
    else:
        standings_by_time = pd.concat([standings_by_time, current_standings], axis=1)

plt.figure(figsize=(12, 12))  # make plot sufficient size

for driver in all_drivers:  # go through all the drivers and plot their cumulative points by time on the graph
    data = standings_by_time.loc[driver].to_list()
    plt.plot([i for i in range(0, len(all_races))], data, label=driver, c=driver_colors[driver])

# add a legend to the plot then show it
plt.legend(bbox_to_anchor=(0.2, 1))
plt.show()
