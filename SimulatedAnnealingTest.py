import matplotlib.pyplot as plt
import numpy
import random
import math


'''BE WARNED: THIS CODE TAKES A

            ___VERY___

LONG TIME (30 mins or so)'''

#graph how changing initial temp changes stuff
#graph how changing templength changes stuff
#graph how temp mult changes stuff
#graph how nonimprovementmax changes stuff

#graph how the best settings from above calculate the local minima (print every kemeny score output)
# First, open file and gather data and start a timer, collect input args

#Generate vars
class Tournament:
    NumberOfGames = 0
    NumberOfParticipants = 0
    InitialTemperature = 0
    CurrentTemperature = 0
    TemperatureMultiplier = 0
    num_non_improve = 0
    TemperatureLength = 0
    KemenyScoreVal = 0
    CostDifference = 0
    NewKemenyScoreVal = 0
    BestKemenyScore = 0
    ChangeOfCost = 0

    #Define init and collect input args
    def __init__(self, NumberOfGames, NumberOfParticipants, Scores, Players, temp, templength, tempmult,
                 nonimprovementmax):

        self.NumberOfGames = NumberOfGames
        self.NumberOfParticipants = NumberOfParticipants
        self.Scores = Scores
        self.Players = Players
        self.InitialTemperature = temp
        self.CurrentTemperature = temp
        self.TemperatureMultiplier = tempmult
        self.TemperatureLength = templength
        self.num_non_improve = nonimprovementmax
        self.KemenyScoreVal = 0
        self.NewKemenyScoreVal = 0
        self.CostDifference = 0
        self.ChangeOfCost = 0
        self.Participants = {}
        self.Ranking = []
        self.BestRanking = []
        self.Neighbour = []
        self.kemenies = []
        self.temps = []
        #Code below sets up the algorithm
        self.InstantiateParticipants()
        self.AssignScores()
        self.AssignRanking()
        self.KemenyScoreVal = self.KemenyScore(self.Ranking)
        self.BestKemenyScore = self.KemenyScoreVal
        #print(self.KemenyScoreVal)
        self.SimulatedAnnealing()

    #Generate a participant for every participant in the race
    def InstantiateParticipants(self):

        for num, name in self.Players:
            self.Participants[int(num)] = Participant(int(num), name)

    #Assign each participant the players they beat and by how much
    def AssignScores(self):

        for numWins, winner, loser in self.Scores:
            self.Participants[int(winner)].WonAgainst.append(int(loser))
            self.Participants[int(winner)].NumWinsAgainst.append(int(numWins))

    #Generate X0
    def AssignRanking(self):

        # ranking is a list of participant ID's from highest to lowest SUM of wins of those participants
        ParticipantWins = []
        for key in self.Participants.keys():
            ParticipantWins.append((self.Participants[key].number, sum(self.Participants[key].NumWinsAgainst)))

        ParticipantWins = sorted(ParticipantWins, key=lambda x: x[1])
        ParticipantWins.reverse()

        for player, score in ParticipantWins:
            self.Ranking.append(player)

        self.Neighbour = self.Ranking.copy()

    #calculate Kemeny score
    def KemenyScore(self, PossibleSolution):

        KemenyScoreVal = 0
        for winnerCheck in PossibleSolution:
            for loserCheck in PossibleSolution:
                #if the loser was ahead of the winner in the ranking but lost to the winner
                if loserCheck in self.Participants[winnerCheck].WonAgainst and PossibleSolution.index(
                        loserCheck) < PossibleSolution.index(winnerCheck):
                    playerIndex = self.Participants[winnerCheck].WonAgainst.index(loserCheck)
                    weight = self.Participants[winnerCheck].NumWinsAgainst[playerIndex]
                    KemenyScoreVal = KemenyScoreVal + weight

        return KemenyScoreVal


    #Choose a Neighbour by choosing 3 racers and swap them around
    def ChooseNeighbour(self):

        # do some permutation of Ranking
        # set it to self.Neighbour
        self.Neighbour = self.Ranking.copy()
        self.NewKemenyScoreVal = self.KemenyScoreVal
        Racers = random.sample(self.Ranking, 3)
        indexes = []
        for racer in Racers:
            indexes.append(self.Ranking.index(racer))
        Racers.insert(0, Racers[len(Racers) - 1])
        Racers.pop(len(Racers) - 1)
        for RacerIndex, NeighbourIndex in enumerate(indexes):
            self.Neighbour[NeighbourIndex] = Racers[RacerIndex]
        #print(self.KemenyScore(self.Neighbour))

        # compute cost difference

        '''MinIndex = min(indexes)
        MaxIndex = max(indexes)
        OldCostInterval = self.KemenyScore(self.Ranking[MinIndex:MaxIndex])
        NewCostInterval = self.KemenyScore(self.Neighbour[MinIndex:MaxIndex])
        self.ChangeOfCost = OldCostInterval - NewCostInterval
        self.NewKemenyScoreVal = (self.KemenyScoreVal - OldCostInterval) + NewCostInterval'''

    def SimulatedAnnealing(self):

        '''''''''''''''''''''''''''''''''''''''''''''

                       THE SA ALGORITHM

        '''''''''''''''''''''''''''''''''''''''''''''

        # Initial solution = self.Ranking
        # Initial temp set in init

        #Set non improvements
        NonImprovements = 0
        while NonImprovements < self.num_non_improve:
            if NonImprovements % 100 == 0:
                print(self.BestKemenyScore)
            #run the loop a number of times equal to temp length
            for i in range(1, self.TemperatureLength):
                #generate a neighbour
                self.ChooseNeighbour()
                #calculate cost change
                CostChange = self.KemenyScore(self.Neighbour) - self.KemenyScore(self.Ranking)
                #accept new state clause
                if CostChange <= 0:
                    self.Ranking = self.Neighbour.copy()
                    self.KemenyScoreVal = self.KemenyScore(self.Ranking)
                    NonImprovements = 0
                else:
                    #randomly accept new state clause
                    q = random.uniform(0, 1)
                    if q < math.e ** -(CostChange / self.CurrentTemperature):
                        self.Ranking = self.Neighbour.copy()
                        NonImprovements += 1
                    else:
                        #reject state clause
                        NonImprovements += 1
                #set best ranking clause
                if self.KemenyScore(self.Ranking) < self.BestKemenyScore:
                    self.BestKemenyScore = self.KemenyScore(self.Ranking)
                    self.BestRanking = self.Ranking


            self.kemenies.append(self.KemenyScore(self.Ranking))
            self.temps.append(self.CurrentTemperature)
            self.CurrentTemperature = self.CurrentTemperature * self.TemperatureMultiplier

        #print(self.BestRanking)
        #print(self.BestKemenyScore)

#Participant class for each player
class Participant:
    number = 0
    name = "name"
    Ranking = 0

    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.WonAgainst = []
        self.NumWinsAgainst = []

file = open("Formula_One_1984.wmg", "r")
contents = file.readlines()
file.close()

# Create a list of relevant data from the file
ScoreList = []
Racers = []

#make list of every racer
for index, line in enumerate(contents):
    if index > 0 and index < 36:
        line = line.split(",")
        line[1] = line[1][0:len(line[1]) - 2]
        Racers.append(line)

#make list of every racers scores
for index, line in enumerate(contents):
    if index > 36:
        line = line.split(",")
        line[2] = line[2][0:len(line[2]) - 1]
        ScoreList.append(line)

temps = []
kemenyfortemps = []

for i in range(10000, 100000, 10000):
    temps.append(i)
    T = Tournament(16, len(Racers), ScoreList, Racers, i, 70, 0.95, 1000)
    kemenyfortemps.append(T.BestKemenyScore)

templengths = []
kemenyfortemplengths = []

for i in range(10, 100, 10):
    templengths.append(i)
    T = Tournament(16, len(Racers), ScoreList, Racers, 10000, i, 0.95, 1000)
    kemenyfortemplengths.append(T.BestKemenyScore)

tempmults = []
kemenyfortempmults = []

for i in range(80, 100, 1):
    tempmults.append(i/100)
    T = Tournament(16, len(Racers), ScoreList, Racers, 10000, 70, i/100, 1000)
    kemenyfortempmults.append(T.BestKemenyScore)

nonimprovements = []
kemenyfornonimprovements = []

for i in range(1000, 2000, 1000):
    nonimprovements.append(i)
    T = Tournament(16, len(Racers), ScoreList, Racers, 10000, 70, 0.95, i)
    kemenyfornonimprovements.append(T.BestKemenyScore)

besttempindex = kemenyfortemps.index(min(kemenyfortemps))
besttemplengthindex = kemenyfortemplengths.index(min(kemenyfortemplengths))
besttempmultsindex = kemenyfortempmults.index(min(kemenyfortempmults))
bestnonimprovementsindex = kemenyfornonimprovements.index(min(kemenyfornonimprovements))

besttemp = temps[besttempindex]
besttemplength = templengths[besttemplengthindex]
besttempmult = tempmults[besttempmultsindex]
bestnonimprovements = nonimprovements[bestnonimprovementsindex]

T = Tournament(16, len(Racers), ScoreList, Racers, besttemp, besttemplength, besttempmult, bestnonimprovements)
print(T.BestKemenyScore)

figure, axs = plt.subplots(3,2)

axs[0, 0].plot(temps, kemenyfortemps)
axs[0, 1].plot(templengths, kemenyfortemplengths)
axs[1, 0].plot(tempmults, kemenyfortempmults)
axs[1, 1].plot(nonimprovements, kemenyfornonimprovements)

T = Tournament(16, len(Racers), ScoreList, Racers, 1000000, 80, 0.95, 5000)
plt.plot(T.temps, T.kemenies)

plt.show()
