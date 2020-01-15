import random
from classes.amino import Amino
from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient, get_score
from functions.GetLegalMoves import get_legal_moves
import copy

best_score = 1
best_chain = None
best_matrix = None

def depth_search(protein, ch_score):
    char_counter = 1

    # Skips the first char the index.
    while protein.char_counter < len(protein.amino_string):

        # print(str(self.char_counter))
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
            ideal_chain = fold_selector(amino_xy, char, protein.chain, illegal_folds, protein.amino_string, ch_score)


        # Ideal chain is already found, replace chain with ideal chain and break loop.
        if ideal_chain:
            for amino in best_chain:
                print(amino)

            protein.matrix, protein.chain = get_matrix(best_chain)
            break


        # Adds amino to the protein chain.
        protein.chain.append(Amino(char, fold, amino_xy))
        char_counter += 1



# The actual algo for selecting the fold the chain will make.
def fold_selector(xy, char, chain, illegal_moves, chars, ch_score):

    # This is the recursive functions which does the depth search.
    find_best_chain(chain, chars, ch_score)

    # IF the algo has actually found the best chain (which it should), return the best chain.
    if best_chain:
        return (True)


    raise Exception("Couldn't find best chain")

# The recursive function which accepts the variables: the current chain of aminos, and the string of the aminos it has yet to process.
def find_best_chain(current_chain, chars, ch_score):

    # The first char has to be popped because it processes that char in the last loop
    # Note: popping the first loop is also valid because the first char is build before loading the fold_selector.
    chars = chars[1:]

    # If there is only 1 char left we've arrived at the end of a chain.
    if len(chars) == 1:

        # Add the last char to the amino chain.
        current_chain.append(Amino(chars[0], 0, current_chain[-1].get_fold_coordinates()))


        # Calculate the matrix (needed for the score.) and the score
        matrix, xy_offset = get_matrix_efficient(current_chain)
        score = get_score_efficient(current_chain, matrix, xy_offset, ch_score)

        global best_score
        global best_chain


        # IF this score is the best score, save this score + chain as a global.
        if score < best_score:
            print("New best score: " + str(score))
            best_score = score
            best_chain = copy.deepcopy(current_chain)


        # Abort that chain if it isnt the best score.
        del current_chain[-1]
        return None

    # Get legal moves on the position of that amino
    legal_moves = get_legal_moves(current_chain[-1].get_fold_coordinates(), current_chain)


    # If no legals move left, abort the chain. The protein got "stuck"
    if not legal_moves:
        return None

    # Go recursively through all legal moves and its child legal moves etc.
    else:
        for move in legal_moves:

            # Find best chain needs a new updated chain, but the old chain also needs to be remembered.
            last_amino = current_chain[-1]
            current_chain.append(Amino(chars[0], move, last_amino.get_fold_coordinates()))
            find_best_chain(current_chain, chars, ch_score)
            del current_chain[-1]