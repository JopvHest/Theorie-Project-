import random
from classes.amino import Amino
from algorithms.helpers import get_matrix, get_score


def random_search(protein):

    while protein.char_counter < len(protein.amino_string):

        char = protein.amino_string[protein.char_counter]
        # Get the location the last amino folded to.
        # Note: an index of -1 gets the last object in a list.
        amino_xy = protein.chain[-1].get_fold_coordinates()

        # Last amino always has fold of 0.
        if protein.char_counter + 1 == len(protein.amino_string):
            fold = 0

        # Determine which fold to pick
        else:
            illegal_folds = None
            fold = fold_selector(amino_xy, char, protein.chain, illegal_folds)

             # If no legal moves are available, the last move needs to be reversed.
            if not fold:
                redo_last_fold(protein)
                continue

        # Adds amino to the protein chain.
        protein.chain.append(Amino(char, fold, amino_xy))
        protein.char_counter += 1

    protein.matrix, protein.chain = get_matrix(protein.chain)

# The actual algo for selecting the fold the chain will make.
def fold_selector(xy, char, chain, illegal_moves):

    legal_moves = get_legal_moves(xy, chain)

    # Remove illegal moves from legal moves list.
    if illegal_moves:
        for move in illegal_moves:
            if move in legal_moves:
                legal_moves.remove(move)

    # Selects a random move if at least 1 legal moves exists. Returns False for no ideal_chain found.
    if legal_moves:
        return random.choice(legal_moves)

    # If no legal moves exist, return False
    return False

def redo_last_fold(protein):
    # Store the illegal fold in the amino class.
    last_amino = protein.chain[-1]
    last_amino.illegal_folds.append(last_amino.fold)

    # Get new move with illegal moves excluded.
    fold = fold_selector(last_amino.coordinates, last_amino.atype, protein.chain[:-1], last_amino.illegal_folds)

    # Replace the previous illegal fold with a new fold
    last_amino.fold = fold


    # If still no fold found, also redo move before that. Char loop in init needs to go back 1 step.
    if not fold:
        protein.chain.remove(last_amino)
        protein.char_counter -= 1
        redo_last_fold(protein)


# Finds all the legal moves that can be made from the current position.
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
