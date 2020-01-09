import random
from classes.amino import Amino, get_matrix, get_score
from pandas import DataFrame
import copy

best_score = 1
best_chain = None

# The actual algo for selecting the fold the chain will make.
def fold_selector(xy, char, chain, illegal_moves, chars):


    find_best_chain(chain, chars)

    if best_chain:
        return (True, best_chain)

    raise Exception("Couldn't find best chain")

def find_best_chain(current_chain, chars):
    chars = chars[1:]

    if len(chars) == 1:
        current_chain.append(Amino(chars[0], 0, current_chain[-1].get_fold_coordinates()))
        matrix, current_chain = get_matrix(current_chain)

        '''
        for amino in current_chain:
            print(amino, end="")
        print("")
        '''


        score = get_score(current_chain, matrix)

        global best_score
        global best_chain
        # print(score)

        if score < best_score:
            print("New best score: " + str(score))
            best_score = score
            best_chain = current_chain

        return None


    legal_moves = get_legal_moves(current_chain[-1].get_fold_coordinates(), current_chain)


    # If no legals move left, stop the chain.
    if not legal_moves:
        return None

    else:
        for move in legal_moves:
            new_chain = copy.deepcopy(current_chain)
            new_chain.append(Amino(chars[0], move, current_chain[-1].get_fold_coordinates()))
            find_best_chain(new_chain, chars)


# Finds all the legal moves that can be made from the current position.
# Returns False for no ideal chain found.
def get_legal_moves(xy, chain):

    # This is a list of tuples with 1: the move, 2: the coordinates delta that cant exist yet.
    moves_xydelta = [[1, (1, 0)], [-1, (-1, 0)], [2, (0, 1)], [-2, (0, -1)]]

    # Check if the legal moves interfere with any of the current amino coordinates.
    # Note: we iterate over a COPY of the list because you cant delete items from a list while iterating over it.
    for amino in list(chain):
        # Check for every legal move left.
        for move in moves_xydelta:

            # If the move delta plus current xy is equal to another amino's xy remove it from the legal moves list.
            coordinates_sum = []
            coordinates_sum.append(move[1][0] + xy[0])
            coordinates_sum.append(move[1][1] + xy[1])

            if coordinates_sum == list(amino.coordinates):
                moves_xydelta.remove(move)

    # Only return the move int of the legal moves remaining.
    legal_moves = []
    for moves in moves_xydelta:
        legal_moves.append(moves[0])

    return legal_moves