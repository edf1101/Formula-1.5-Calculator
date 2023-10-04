import pandas as pd


class _Standings:

    # Constructor for standings class just initialised the driver + constructor standings dataframes
    def __init__(self, all_drivers, all_teams):
        driver_standing_dict = {'Driver': all_drivers,
                                'Points': [0] * len(all_drivers)}
        self._driverTable = pd.DataFrame(driver_standing_dict).set_index('Driver')

        team_standing_dict = {'Team': all_teams,
                              'Points': [0] * len(all_teams)}
        self._constructorTable = pd.DataFrame(team_standing_dict).set_index('Team')

    def add_to_standings(self, data):
        for i in data.index:
            self._driverTable['Points'][i] += data['Points'][i]
            self._constructorTable['Points'][data['Team'][i]] += data['Points'][i]

        self._driverTable = self._driverTable.sort_values('Points', ascending=False)
        self._constructorTable = self._constructorTable.sort_values('Points', ascending=False)

    def getConstructorTable(self):
        return self._constructorTable

    def getDriverTable(self):
        return self._driverTable


class Season:

    def __init__(self, banned_teams, race_path, sprint_path="", modify_points=None):
        # Assign the parameters
        self._racePath = race_path
        self._sprintPath = sprint_path  # optional parameter as there may not be sprint race data
        self._bannedTeams = banned_teams

        # set up the race data
        self._raceData = None
        self._sprintData = None
        self._setupRaceData()

        # Set up lists of all drivers / teams / tracks
        self._allRaces = None
        self._allSprints = None
        self._allTeams = None
        self._allDrivers = None
        self._getAllOptions()

        # set up race points data the [0] * 100 means can in theory support up to 100 drivers
        self._pointsRace = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1] + ([0] * 100)
        if modify_points is not None:  # If modifying points then swap over
            self._pointsRace = modify_points
        self._pointsSprint = [8, 7, 6, 5, 4, 3, 2, 1, 0, 0] + ([0] * 100)

        # Calculate all new race results
        self._newRaces ={}
        self._newSprints = {}

        for race in self._allRaces:
            self._newRaces[race] = self._calculateRaceScoreboard(race,False)

        if (self._sprintPath != ""):
            for sprint in self._allSprints:
                self._newSprints[sprint] = self._calculateRaceScoreboard(sprint,True)


    # Functions for setting up season data
    def _setupRaceData(self):
        self._raceData = pd.read_csv(self._racePath)

        if (self._sprintPath != ""):  # if sprint races have been assigned
            self._sprintData = pd.read_csv(self._sprintPath)

    def _getAllOptions(self):
        self._allRaces = list(dict.fromkeys(self._raceData['Track']))

        if self._sprintPath !="": # Do we have sprint data
            self._allSprints = list(dict.fromkeys(self._sprintData['Track']))

        # Mask out the banned teams, so we only have drivers and teams excluding them
        bannedTeamMask = (~self._raceData['Team'].isin(self._bannedTeams))
        self._allTeams = list(dict.fromkeys(self._raceData[bannedTeamMask]['Team']))
        self._allDrivers = list(dict.fromkeys(self._raceData[bannedTeamMask]['Driver']))

    # Functions for calculating individual race data

    def _getRaceData(self, race, input_data):

        # mask out unwanted teams and unwanted data columns
        bannedTeamMask = (~input_data['Team'].isin(self._bannedTeams))
        interesting_columns = ['Track', 'Position', 'Driver', 'Team', 'Points', 'Fastest Lap Time']

        _specific_race_data = input_data[(input_data['Track'] == race) & bannedTeamMask].filter(interesting_columns)
        _specific_race_data = _specific_race_data.copy()
        return _specific_race_data

    def _redo_positions(self, _specific_race_data): # reorders the positions of those remaining after banned teams out

        not_classified_count = _specific_race_data['Position'].tolist().count('NC') # those who didn't finish
        drivers_in_race = len(_specific_race_data['Position']) - not_classified_count

        new_positions = list(range(1, drivers_in_race + 1)) + (['NC'] * not_classified_count)
        _specific_race_data['Position'] = new_positions

        return _specific_race_data.copy()

    def _get_fastest_driver(self, _specific_race_data):
        fastest_lap = _specific_race_data['Fastest Lap Time'].sort_values().iloc[0]
        _fastest_driver = _specific_race_data[(_specific_race_data['Fastest Lap Time'] == fastest_lap)]
        return _fastest_driver

    def _make_scoreboard(self, _specific_race_data, _fastest_driver, isSprint):

        pointsSystem = self._pointsRace # use default point system unless sprint
        if(isSprint):
            pointsSystem = self._pointsSprint

        not_classified_count = _specific_race_data['Position'].tolist().count('NC')
        drivers_in_race = len(_specific_race_data['Position']) - not_classified_count
        new_points = [0] * (not_classified_count + drivers_in_race)

        # add points for all classified drivers
        for i in range(drivers_in_race):
            position = _specific_race_data.iloc[i]['Position']
            new_points[i] = pointsSystem[position - 1]

        if (isSprint == False and (_fastest_driver['Position'].iloc[0], int) and _fastest_driver['Position'].iloc[0] <= 10):
            new_points[_fastest_driver['Position'].iloc[0] - 1] += 1

        _specific_race_data['Points'] = new_points
        _specific_race_data = _specific_race_data.copy()
        return _specific_race_data


    def _calculateRaceScoreboard(self, race_name, isSprint = False):
        # race_name is the text name of race, isSprint is bool for if sprint race or not

        race_data = self._raceData # race data is normal race by default unless isSprint then its sprint data
        if(isSprint):
            race_data = self._sprintData

        # create and modify the race data
        race_dataset = self._getRaceData(race_name,race_data)
        race_dataset = self._redo_positions(race_dataset)

        # Ignore fastest driver stuff if its a sprint race
        fastest_driver=None
        if (isSprint == False):
            fastest_driver = self._get_fastest_driver(race_dataset)

        # create the scoreboard
        scoreboard = self._make_scoreboard(race_dataset, fastest_driver,isSprint)
        scoreboard = scoreboard.filter(['Driver', 'Team', 'Points']) # only include these columns
        scoreboard = scoreboard.set_index('Driver')
        return scoreboard

    def getRaceScoreboard(self,race): # getter for newRaces dict
        return self._newRaces[race]

    def getSprintScoreboard(self,race): # getter for newRaces dict
        return self._newSprints[race]

    def getStandings(self, calendar = None): # function to get standings after a number of races (defualt is a season)
        # set up the standings
        seasonStandings = _Standings(self._allDrivers, self._allTeams)

        if calendar is None: # if no supplied special calendar then use whole calendar
            calendar = self._allRaces

        for race in calendar:
            seasonStandings.add_to_standings(self.getRaceScoreboard(race))

            # check if its a sprint weekend if so add on points
            if self._sprintPath!="" and  race in self._allSprints:
                seasonStandings.add_to_standings(self.getSprintScoreboard(race))

        return seasonStandings

    # Other getters
    def getAllDrivers(self):
        return self._allDrivers

    def getAllSprints(self):
        return self._allSprints

    def getAllRaces(self):
        return self._allRaces

    def getAllTeams(self):
        return self._allTeams