
import copy
from classes.amino import Amino
from classes.chain import Chain
from functions.GetLegalMoves import get_legal_moves
import random


def iterative_algorithm(chain, iterations):

    # take the chain
    chain_actual = chain.chain_list

    # determine max index and make list of all possible indexes
    max_index = len(chain_actual) - 1
    
    # skip last because does not fold to a new one
    indexes = list(range(0, max_index - 1))
    changes = 0
    # do n iterations
    while changes != iterations:

        # get random amino by randomizing indexes
        random_index = random.choice(indexes)
        amino_actual = chain_actual[random_index]

        # select possible folds
        coordinates = amino_actual.coordinates
        legal_moves = get_legal_moves(coordinates, chain_actual)

        # remove the current fold fromm possibilities
        current_fold = amino_actual.fold
        if current_fold in legal_moves:
            legal_moves.remove(current_fold)
        
        # if there are no legal moves start again
        if not legal_moves:
            continue
        else:
            # change fold of the amino
            new_fold = random.choice(legal_moves)
            amino_actual.fold = new_fold
            # get the amino after the selected amino and get fold and coordinates
            amino_next = chain_actual[random_index + 1]
            amino_next.coordinates = amino_actual.get_fold_coordinates()
            fold_next = amino_next.fold
            
            # if equal to max index, last amino is refolded
            if random_index == max_index:
                changes += 1
                continue

            # diffrentiate between 2 folds in same direction and different direction
            if new_fold == fold_next:
                # inverse folds
                amino_next.fold = current_fold
            
            else:
                
                # inverse folds
                amino_next.fold = current_fold
                coordinates_to_check = amino_next.get_fold_coordinates()
                for amino in chain_actual:
                    if coordinates_to_check == amino.coordinates:
                        continue
                
                amino_after_next = chain_actual[random_index + 2]
                amino_after_next.coordinates = coordinates_to_check

                # is the opposite of the first new fold
                amino_after_next.fold = new_fold * -1




                pull_chain(chain_actual, 2, random_index)
                
            changes += 1


# function to pull in the chain by changing fold and coordinates
def pull_chain(chain, number_changes, index):

    # go trough all aminos in te chain until aminos left equal to number of changes
    for i in range(index + 1, len(chain) - number_changes - 1):
        chain_unchanged = copy.deepcopy(chain)
        amino_changed = chain_unchanged[i]
        amino_pulled = chain[i + number_changes]

        amino_pulled.coordinates = amino_changed.coordinates
        amino_pulled.fold = amino_changed.fold
    return chain

