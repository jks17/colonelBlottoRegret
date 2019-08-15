from itertools import product
import numpy as np
import random 

def get_all_strategies(num_battlefields, num_soldiers):
    perm = list(product(np.arange(num_soldiers + 1), repeat=num_battlefields))
    moves = [i for i in perm if np.sum(i) == num_soldiers]

    return moves


def select_strategy(all_strategies, regret_vector):

    # Make negative numbers zero 
    pos_regret_vector = [val if val > 0 else 0 for val in regret_vector]
    # if all zeros in vector - make uniform probability distribution
    if np.count_nonzero(pos_regret_vector) == 0:
        probabilities = np.ones(
            len(pos_regret_vector)) / len(pos_regret_vector)

    # turn regret vector into probability vector if not all zeros.
    else:
        probabilities = pos_regret_vector / np.sum(pos_regret_vector)

    r = random.uniform(0, 1)
    total = 0
    for idx, val in enumerate(probabilities):
        total += val
        if r < total:
            return all_strategies[idx], idx

    return ('error in selecting strategy')



def game_outcome(player1_move, player2_move):

    if len(player1_move) != len(player2_move):
        print('different number of battlefields for each player')
        return

    wins_p1 = 0
    wins_p2 = 0
    for p1, p2 in zip(player1_move, player2_move):
        if p1 > p2:
            wins_p1 += 1
        elif p2 > p1:
            wins_p2 += 1

    if wins_p1 > wins_p2:
        return +1
    elif wins_p2 > wins_p1:
        return -1
    else:
        return 0
    
    
    
def update_regret_vector(regret_vector, all_strategies, your_strategy,
                         opponents_strategy):

    utility_of_strategy = game_outcome(your_strategy, opponents_strategy)

    updated_regret_vector = [
        val + (game_outcome(all_strategies[idx], opponents_strategy) -
               utility_of_strategy) for idx, val in enumerate(regret_vector)
    ]

    return updated_regret_vector