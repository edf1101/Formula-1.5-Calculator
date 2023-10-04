'''
This example shows the ability of the f1point5 library to adjust modern f1 Races to alternate points systems
In this example we are combining the normal (non sprint) races from the 2023 with the points system from 1991 to 2002
The System allocated points as such:
1st - 10      2nd - 6       3rd - 4       4th - 3       5th - 2       6th - 1     and 0 to the remainders
'''

import f1point5 as f1

old_points_system = [10, 6, 4, 3, 2, 1, 0, 0, 0, 0] + ([0] * 100)  # an array allocating what positions get what points

banned_teams = []  # In this example we aren't banning teams

# Race data from 2023 up to the Japanese Grand Prix
race_data_address = "data/Formula1_2023season_raceResults.csv"

# create the season  with modified points
season_2023 = f1.Season(banned_teams, race_data_address, modify_points=old_points_system)
season_standings = season_2023.getStandings()  # get standings

# print the seasons driver championship standings so far with old points system
print(season_standings.getDriverTable())
