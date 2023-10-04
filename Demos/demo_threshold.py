'''
Formula 1.5 is often referred to as determine the "Best of the Rest". In other words, excluding the top teams in
Formula 1 that are unreachable by the rest of the field.
This demo initially calculates the normal standings including all teams. Then gets the range of points between the
highest and lowest scoring team. Any team who's constructor points are above a certain threshold  (in this example
45% of the range is the threshold) is marked as a outlier team and is excluded when calculating the F1.5 standings
'''

import f1point5 as f1


# Race & Sprint data from 2023 up to the Japanese Grand Prix
race_data_address = "data/Formula1_2023season_raceResults.csv"
sprint_data_address = "data/Formula1_2023season_sprintResults.csv"

banned_teams = []  # At the moment we want the normal F1 standings so we don't ignore any teams
original_season = f1.Season(banned_teams, race_data_address, sprint_data_address) # create the season race & standing data
original_season_standings = original_season.getStandings()


# calculate the range of points
original_points = original_season_standings.getConstructorTable()['Points']
lowest_points = original_points.iloc[len(original_points)-1] # sorted descendingly so team with lowest points is last
highest_points = original_points.iloc[0]
points_range = highest_points-lowest_points

threshold = lowest_points+ (0.45 * points_range) # calculate the threshold as the 45th percentile in this example


# calculate outliers by getting the original standings and finding any teams who's points are above the threshold
outliers = original_season_standings.getConstructorTable()[original_points >threshold].index

f1point5_season = f1.Season(outliers,race_data_address,sprint_data_address)

f1point5_standings = f1point5_season.getStandings()
# Print the F1.5 driver standings
print(f1point5_standings.getDriverTable())

# Or for constructor standings
print(f1point5_standings.getConstructorTable())

