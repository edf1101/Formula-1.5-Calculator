import pandas as pd

raceDataAddress ="Formula1_2023season_raceResults.csv"
sprintDataAddress = ''

race_data = pd.read_csv(raceDataAddress)
print(race_data.head())