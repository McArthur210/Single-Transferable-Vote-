# Simulates an election under Single Transferable Vote using the Gregory Method to distribute surplus votes, Droop as the quota, and backwards tie-breaking. 

import random

class Ballots: # ballot storage 
    def __init__(self, names, weight):
        self.names = names # names of all the candidates on each ballot 
        self.weight = weight # how much each ballot counts (less than or equal to 1; only changes when a candidate has a surplus of votes)

class Person: # assigns and manages ballots to candidates 
    def __init__(self, name):
        self.name = name
        self.my_ballots = []

    def setBallots(self, all_ballots):
        for ballot in all_ballots:
            if ballot.names[0] == self.name: # checks if the choice on the ballot matches its respective candidate 
                self.my_ballots.append(ballot) # adds ballot to a candidate's total number of ballots

def count_votes(round_snapshot,round_counter): # counts the total WEIGHT of each vote for each candidate 
    new_round = []
    if round_counter == 0:
        for y in range(0,len(candidates)):
            total = 0
            for x in range(0,len(candidates[y].my_ballots)):
                total += (candidates[y].my_ballots[x]).weight
            new_round.append(total)
        round_snapshot.append(new_round)
    else:
        for y in range(0,len(candidates)):
            if round_snapshot[round_counter][y] == 0:
                total = 0
                new_round.append(total)
            else:
                total = 0
                for x in range(0,len(candidates[y].my_ballots)):
                    total += (candidates[y].my_ballots[x]).weight # adds the total weight of each candidate 
                new_round.append(total)
        round_snapshot.append(new_round) # creates new round 

    return round_snapshot 

def find_min(round_snapshot,round_counter): # finds the least votes 
    min_vote = round_snapshot[round_counter][0]
    for x in range(1,(len(round_snapshot[round_counter]))):
        if (min_vote > round_snapshot[round_counter][x]) and not(round_snapshot[round_counter][x] == 0):
            min_vote = round_snapshot[round_counter][x]
    
    return min_vote
                
def redistribute_loser(candidates,loser,candidate_names,round_snapshot,round_counter):
    loser_list = []
    for t in range(0,len(candidates)):
        if round_snapshot[round_counter][t] == 0:
            losers = candidates[t].name
            loser_list.append(losers)
    for ballot in loser.my_ballots: # goes through ballots of loser candidate
        counter = 0
        invalid = 1
        while invalid and (counter < len(candidates)):
            if ballot.names[counter] == loser.name:
                counter += 1
            elif ballot.names[counter] in loser_list: # prevents the program from giving ballots to people already eliminated or nominated
                counter += 1
            else:
                invalid = 0
        if counter == len(candidates): # the ballot is exhausted and cannot go anywhere else (i.e. the voter did not rank all of the candidates or it is the last round)
            pass
        else:
            for candidate in candidates:
                if candidate.name == ballot.names[counter]: # checks for the ballot's next choice candidate
                    candidate.my_ballots.append(ballot) # transfers the ballot to the next candidate

def finish_elimination(candidates,candidate_names,round_snapshot,round_counter,losers_index):
    redistribute_loser(candidates,candidates[losers_index[0]],candidate_names,round_snapshot,round_counter)
    round_snapshot = count_votes(round_snapshot,round_counter)
    round_counter += 1 
    round_snapshot[round_counter][losers_index[0]] = 0 # lets the program know that the candidate has been elected/eliminated and cannot receive nor give votes anymore 

    return round_snapshot, round_counter

def find_max(round_snapshot,round_counter): # finds the greatest votes
    max_vote = round_snapshot[round_counter][0]
    for x in range(1,(len(round_snapshot[round_counter]))):
        if (max_vote < round_snapshot[round_counter][x]) and not(round_snapshot[round_counter][x] == 0):
            max_vote = round_snapshot[round_counter][x]
    
    return max_vote

def redistribute_winner(candidates,winner,candidate_names,round_snapshot,round_counter,winners_index):
    loser_list = []
    new_multi = (round_snapshot[round_counter][winners_index[0]] - quota) / round_snapshot[round_counter][winners_index[0]] # calculates the multiplier for the votes of the elected candidate
    for t in range(0,len(candidates)):
        if round_snapshot[round_counter][t] == 0:
            losers = candidates[t].name
            loser_list.append(losers)
    for ballot in winner.my_ballots: # goes through ballots of winner candidate; goes through each candidate of a ballot until the next candidate of its respective ballot is found
        counter = 0
        invalid = 1
        while invalid and (counter < len(candidates)):
            if ballot.names[counter] == winner.name: # prevents the program from giving ballots to the candidate that had just been nominated 
                counter += 1
            elif ballot.names[counter] in loser_list: # prevents the program from giving ballots to people already eliminated or nominated 
                counter += 1
            else:
                invalid = 0
        if counter == len(candidates): # the ballot is exhausted and cannot go anywhere else (i.e. the voter did not rank all of the candidates or it is the last round)
            pass
        else:
            for candidate in candidates: 
                if candidate.name == ballot.names[counter]: # checks for the ballot's next choice candidate
                    ballot.weight *= new_multi # changes the weight of each ballot of the winning candidate 
                    candidate.my_ballots.append(ballot) # transfers the ballot to the next candidate 

def finish_nomination(candidates,candidate_names,round_snapshot,round_counter,winners_index):
    redistribute_winner(candidates,candidates[winners_index[0]],candidate_names,round_snapshot,round_counter,winners_index)
    round_snapshot = count_votes(round_snapshot,round_counter)
    round_counter += 1
    round_snapshot[round_counter][winners_index[0]] = 0

    return round_snapshot, round_counter
    
num_seats = int(input('Enter the number of seats -> ')) # sets the number of seats available for the election 
while num_seats < 3: # prevents there being less than 3 seats 
    num_seats = int(input('Error! Re-enter the number of seats -> '))
input_list = input('Enter the list of candidate names -> ')
candidate_names = input_list.split(", ")
while len(candidate_names) < num_seats: # prevents there being less candidates than seats available 
    input_list = input('Error! Re-enter the list of candidates -> ')
    candidate_names = input_list.split(", ")
num_voters = int(input('Enter the number of voters -> ')) # sets the number of voters/ballots for the election 
while num_voters < 1: # must be at least 1 voter 
    num_voters = int(input('Error! Re-enter the number of voters -> ')) 
seed = int(input('Enter the seed -> ')) # sets the value of the seed for the random ballot generator 

random.seed(seed) # makes the data stay the same in order to check the results in future executions of the program 
quota = (num_voters / (num_seats + 1)) + 1 # calculates the droop quota

#Generates random ballots 
ballots = [] # creates initial empty list of ballots 
for i in range(num_voters): # creates a ballot for each voter 
    shuffled_candidate_names = candidate_names.copy() # creates a copy of a ballot 
    random.shuffle(shuffled_candidate_names) # randomly shuffles list of candidates on ballot, with each column representing a candidate's ranking (best to worst from left to right)
    new_ballot = Ballots(shuffled_candidate_names, 1) # adds ballot to class Ballots 
    ballots.append(new_ballot) # adds ballot to list ballots

# Generates people
candidates = [] # creates an initial empty list of candidates; acts as a pool which slowly loses a candidate each round either by eliminating him or her as a loser or a winner
for candidate_name in candidate_names:
    new_candidate = Person(candidate_name)
    candidates.append(new_candidate)

# Assign ballots to candidates
for candidate in candidates:
    candidate.setBallots(ballots)

round_snapshot = [] # list of each candidate's votes during each round 
round_counter = 0 # specifies which round the program is on 

round_snapshot = count_votes(round_snapshot,round_counter)
final_winners = []

while len(final_winners) < num_seats: # checks if all of the seats have been filled 
    winners_index = [] # the index of the candidate who will be nominated in the round 
    for d in range(0,len(candidates)):
        if (round_snapshot[round_counter][d] >= quota) and (round_snapshot[round_counter][d] == find_max(round_snapshot,round_counter)):
            winners_index.append(d)
    if len(winners_index) == 0:
        losers_index = [] # the index of the candidate who will be eleminated in the round 
        for t in range(0,len(candidates)):
            if round_snapshot[round_counter][t] == find_min(round_snapshot,round_counter):
                losers_index.append(t)
        if len(losers_index) == 1:
            round_snapshot, round_counter = finish_elimination(candidates,candidate_names,round_snapshot,round_counter,losers_index)
        else: # multiple candidates are tied to lose 
            if round_counter == 0: # randomly chooses a loser since there are no previous rounds to look at to break the tie 
                losers_index = [random.choice(losers_index)]
                round_snapshot, round_counter = finish_elimination(candidates,candidate_names,round_snapshot,round_counter,losers_index)
            else:
                tie_votes = []
                real_losers = [] 
                pre_counter = round_counter - 1
                while pre_counter >= 0 and (len(losers_index) > 1):
                    for k in range(0,len(losers_index)): # finds the votes of each loser in the previous round
                        pre_losers_votes = round_snapshot[pre_counter][losers_index[k]]
                        tie_votes.append(pre_losers_votes)
                    losers_index = losers_index.copy()
                    for l in losers_index:
                        if round_snapshot[pre_counter][l] == min(tie_votes): # finds the candidate with the least votes out of the tied candidates 
                            real_loser = l
                            real_losers.append(real_loser)
                    losers_index = real_losers
                    pre_counter = pre_counter - 1
                if len(losers_index) > 1: # randomly chooses a loser since there are no more previous rounds to look at to break the tie
                    losers_index = [random.choice(losers_index)]
                    round_snapshot, round_counter = finish_elimination(candidates,candidate_names,round_snapshot,round_counter,losers_index)
                else:
                    round_snapshot, round_counter = finish_elimination(candidates,candidate_names,round_snapshot,round_counter,losers_index)
    elif len(winners_index) == 1:
        final_winners.append(winners_index)
        round_snapshot, round_counter = finish_nomination(candidates,candidate_names,round_snapshot,round_counter,winners_index)
    elif len(winners_index) > 1: # multiple candidates are tied to win 
        if round_counter == 0: # randomly chooses a winner since there are no previous rounds to look at to break the tie
            winners_index = [random.choice(winners_index)]
            final_winners.append(winners_index)
            round_snapshot, round_counter = finish_nomination(candidates,candidate_names,round_snapshot,round_counter,winners_index)
        else:
            tie_votes = []
            real_winners = [] 
            pre_counter = round_counter - 1
            while pre_counter >= 0 and (len(winners_index) > 1):
                for k in range(0,len(winners_index)): # finds the votes of each winner in the previous round 
                    pre_winners_votes = round_snapshot[pre_counter][winners_index[k]]
                    tie_votes.append(pre_winners_votes)
                winners_index = winners_index.copy()
                for l in winners_index:
                    if round_snapshot[pre_counter][l] == max(tie_votes): # finds the candidate with the most votes out of the tied candidates 
                        real_winner = l
                        real_winners.append(real_winner)
                winners_index = real_winners
                pre_counter = pre_counter - 1
            if len(winners_index) > 1: # randomly chooses a winner since there are no more previous rounds to look at to break the tie
                winners_index = [random.choice(winners_index)]
                final_winners.append(winners_index)
                round_snapshot, round_counter = finish_nomination(candidates,candidate_names,round_snapshot,round_counter,winners_index)
            else:
                final_winners.append(winners_index)
                round_snapshot, round_counter = finish_nomination(candidates,candidate_names,round_snapshot,round_counter,winners_index)

print('The winners are:') # Displays the final winners 
for m in range(0,len(final_winners)):
    print(candidates[final_winners[m][0]].name)
