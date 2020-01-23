import random
from classes.amino import Amino
from functions.GetMatrix import get_matrix
from functions.GetScore import get_score
from functions.GetLegalMoves import get_legal_moves


def random_search(protein):

    while protein.char_counter < len(protein.amino_string):
        
        char = protein.amino_string[protein.char_counter]
        # Get the location the last amino folded to.
        # Note: an index of -1 gets the last object in a list.
        amino_xy = protein.chain.chain_list[-1].get_fold_coordinates()

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
        protein.chain.chain_list.append(Amino(char, fold, amino_xy))
        protein.char_counter += 1

    protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)
    print(get_score(protein.chain.chain_list, protein.matrix))

# The actual algo for selecting the fold the chain will make.
def fold_selector(xy, char, chain, illegal_moves):

    legal_moves = get_legal_moves(xy, chain.chain_list)

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
    last_amino = protein.chain.chain_list[-1]
    last_amino.illegal_folds.append(last_amino.fold)

    # Get new move with illegal moves excluded.
    protein.chain.chain_list[:-1]
    fold = fold_selector(last_amino.coordinates, last_amino.atype, protein.chain, last_amino.illegal_folds)

    # Replace the previous illegal fold with a new fold
    last_amino.fold = fold


    # If still no fold found, also redo move before that. Char loop in init needs to go back 1 step.
    if not fold:
        protein.chain.chain_list.remove(last_amino)
        protein.char_counter -= 1
        redo_last_fold(protein)

