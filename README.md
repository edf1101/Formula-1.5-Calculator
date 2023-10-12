# Formula 1.5 Calculator

> Formula 1.5 is a championship within the Formula 1 World Championship to determine the "Best of the Rest". In other words, it is an unofficial championship that excludes the top teams in Formula 1 that are unreachable by the rest of the field

Having just learnt pandas for my Machine Learning Module at University I thought that I'd put it to use to process the F 1.5 Standings for any season given a .csv input of Race/Sprint results.

datasets can be found here : https://github.com/toUpperCase78/formula1-datasets/ thanks to the work of user 'toUpperCase78'

The basics of the code and a bit of documentation can be found in the Jupyter Notebook in the /docs folder

## Features 
- Exclude specifc teams from Driver & Constructor championships and provide correct recalculated standings
- Sprint and Full Race support
- Can code graphing features into it
- Can use different point systems to work with old data
- Pandas dataframe compatible

## Basic Demo
Here is a brief guide on how to use basic functionality, most tools are shown in the demos or aren't too hard to figure out from the library file as its ~200 lines

```
import f1point5 as f1

banned_teams = ['Red Bull Racing Honda RBPT']  # In this example we are only excluding Red Bull

# Race & Sprint data from 2023 up to the Japanese Grand Prix
race_data_address = "data/Formula1_2023season_raceResults.csv"
sprint_data_address = "data/Formula1_2023season_sprintResults.csv"


season_2023 = f1.Season(banned_teams, race_data_address, sprint_data_address) # create the season race & standing data
season_standings = season_2023.getStandings()

# print the seasons driver championship standings so far
print(season_standings.getDriverTable())
```
