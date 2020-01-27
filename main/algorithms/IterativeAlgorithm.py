import copy
import random

from classes.amino import Amino
from classes.chain import Chain
from functions.GetLegalMoves import get_legal_moves


def iterative_algorithm(protein, iterations):

    # take the chain
    chain_actual = protein.chain.chain_list
    chain_actual_copy = copy.deepcopy(chain_actual)

    # determine max index and make list of all possible indexes
    max_index = len(chain_actual) - 1
    
    # skip last because does not fold to a new one
    indexes = list(range(1, max_index - 1))
    changes = 0
    # do n iterations
    while changes != iterations:

        # get random amino by randomizing indexes
        # random_index = random.choice(indexes)
        random_index = 5
        print("index: " + str(random_index))
        amino_actual = chain_actual[random_index]
        print("amino actual: ", amino_actual)
        chain_new = []

        # select possible folds
        coordinates = amino_actual.coordinates
        legal_moves = get_legal_moves(coordinates, chain_actual)


        print("legal moves:")
        print(legal_moves)

        # for i in range(0, random_index - 1):
        #     chain_new.append(chain_actual[i])

        # remove the current fold fromm possibilities
        current_fold = amino_actual.fold
        print("current fold: ", end="")
        print(current_fold)
        if current_fold in legal_moves:
            
            legal_moves.remove(current_fold)
            print("legal moves: ", end="")
            print(legal_moves)

        print("legal moves2:", end='')
        print(legal_moves)
        
        # if there are no legal moves start again
        if not legal_moves:
            chain_actual = chain_actual_copy
            print("no legal moves")
            continue
        else:
            # change fold of the amino
            new_fold = random.choice(legal_moves)
            amino_actual.fold = new_fold
            # chain_new.append(amino_actual)
            
            

            
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

            print("folds:")
            print(new_fold)
            print(new_fold * -1)
            print(current_fold)

            if new_fold * -1 == current_fold:
                chain_actual = chain_actual_copy
                print("abs = abs")
                continue
            
            else:
                
                # inverse folds
                amino_next.fold = current_fold
                coordinates_to_check = amino_next.get_fold_coordinates()
                for amino in chain_actual_copy:
                    if coordinates_to_check == amino.coordinates:
                        # amino_next.fold = fold_next
                        chain_actual = chain_actual_copy
                        print("coordinates overlap")
                        continue
                
                amino_after_next = chain_actual[random_index + 2]
                amino_after_next.coordinates = coordinates_to_check
                
                
                
                # is the opposite of the first new fold
                amino_after_next.fold = new_fold * -1


                # chain_new.append(amino_after_next)
                
                
                # chain_actual = pull_chain(chain_actual, chain_actual_copy, 2, random_index)

                for j in range(0, random_index + 2):
                    chain_new.append(chain_actual[j])


                # go trough all aminos in te chain until aminos left equal to number of changes - 1 to cenvert length list to index length
                # for i in range(random_index + 1, len(chain_actual) - 2):
                #     amino_changed = chain_actual_copy[i]
                #     amino_pulled = chain_actual[i + 2]

                #     amino_pulled.coordinates = amino_changed.coordinates
                #     if amino_pulled.fold == 0:
                #         amino_pulled.fold = 0
                #     else:
                #         amino_pulled.fold = amino_changed.fold
                #     chain_new.append(amino_pulled)
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


# def pull_chain(chain, number_changes, index)

#     new_chain = []

#     for i in range(0, index)
#         new_chain.append(chain[index])
#     for i in range(index + 1, len(chain) - number_changes - 1):
