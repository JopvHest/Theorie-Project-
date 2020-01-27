
import copy
from classes.amino import Amino
from classes.chain import Chain
from functions.GetLegalMoves import get_legal_moves
import random


def iterative_algorithm(protein, iterations):

    # take the chain
    chain_actual = protein.chain.chain_list
    chain_actual_copy = copy.deepcopy(chain_actual)

    # determine max index and make list of all possible indexes
    max_index = len(chain_actual) - 1
    
    # skip last because does not fold to a new one
    indexes = list(range(0, max_index - 1))
    changes = 0
    # do n iterations
    while changes != iterations:

        # get random amino by randomizing indexes
        random_index = random.choice(indexes)
        print("index: " + str(random_index))
        amino_actual = chain_actual[random_index]
        print("amino actual: ", amino_actual)
        chain_new = []

        # select possible folds
        coordinates = amino_actual.coordinates
        legal_moves = get_legal_moves(coordinates, chain_actual)

        # for i in range(0, random_index - 1):
        #     chain_new.append(chain_actual[i])

        # remove the current fold fromm possibilities
        current_fold = amino_actual.fold
        if current_fold in legal_moves:
            legal_moves.remove(current_fold)
        
        # if there are no legal moves start again
        if not legal_moves:
            chain_actual = chain_actual_copy
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
            if random_index + 1 == max_index:
                # chain_new.append(amino_next)
                changes += 1
                continue

            # diffrentiate between 2 folds in same direction and different direction
            if new_fold == fold_next:
                # inverse folds
                amino_next.fold = current_fold
                # chain_new.append(amino_next)

            elif abs(new_fold) == abs(current_fold):
                chain_actual = chain_actual_copy
                continue
            
            else:
                # inverse folds
                amino_next.fold = current_fold
                coordinates_to_check = amino_next.get_fold_coordinates()
                for amino in chain_actual_copy:
                    if coordinates_to_check == amino.coordinates:
                        # amino_next.fold = fold_next
                        chain_actual = chain_actual_copy
                        continue
                
                amino_after_next = chain_actual[random_index + 2]
                amino_after_next.coordinates = coordinates_to_check
                
                # is the opposite of the first new fold
                amino_after_next.fold = new_fold * -1

                for j in range(0, random_index + 2):
                    chain_new.append(chain_actual[j])

                amino_last = chain_actual[-1]
                amino_last.fold = 0
                
            changes += 1
            # return chain_new
            return chain_actual, chain_new


# function to pull in the chain by changing fold and coordinates
def pull_chain(chain, chain_copy, number_changes, index):

    chain_unchanged = chain_copy
    # go trough all aminos in te chain until aminos left equal to number of changes
    for i in range(index + 1, len(chain) - number_changes - 1):
        amino_changed = chain_unchanged[i]
        amino_pulled = chain[i + 1 + number_changes]

        amino_pulled.coordinates = amino_changed.coordinates
        if amino_pulled.fold == 0:
            continue
        else:
            amino_pulled.fold = amino_changed.fold
    return chain
