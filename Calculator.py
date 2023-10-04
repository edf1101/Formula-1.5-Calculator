import f1point5 as f1


# Example data
banned_teams =[]
raceDataAddress ="Formula1_2023season_raceResults.csv"
sprintDataAddress = 'Formula1_2023season_sprintResults.csv'

season2023 = f1.Season(banned_teams,raceDataAddress,sprintDataAddress)
points = season2023.getStandings().getConstructorTable()['Points']
range =points.iloc[0] - points.iloc[len(points)-1]

threshold = 0.4 * range
outliers = season2023.getStandings().getConstructorTable()[points >threshold].index

season2023 = f1.Season(outliers,raceDataAddress,sprintDataAddress)
print(season2023.getStandings().getConstructorTable())

