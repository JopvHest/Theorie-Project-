import random
from classes.amino import Amino
from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient, get_score
from functions.GetLegalMoves import get_legal_moves
import copy

best_score = 1
best_chain = []
current_lookahead = 0

def depth_search_lookahead(protein, max_lookahead, ch_score):
    global best_chain
    global best_score
    chars = protein.amino_string
    chain_length_goal = len(chars)



    # The first char amino is build in the proteine class
    chars = chars [1:]

    # Skips the first char the index.
    while True:

        # print(str(self.char_counter))
        char = chars[0]
        # Get the location the last amino folded to.
        # Note: an index of -1 gets the last object in a list.
        amino_xy = protein.chain[-1].get_fold_coordinates()


        # Last amino always has fold of 0.
        if protein.char_counter + 1 == len(protein.amino_string):
            fold = 0

        # Determine which fold to pick. Ideal chain is returned as true if the full chain is already processed.
        # If ideal_chain is false, the next ideal fold is given.
        else:
            ideal_chain, fold = fold_selector(protein.chain, chars, max_lookahead, chain_length_goal, ch_score)


        # Ideal chain is already found, replace chain with ideal chain and break loop.
        if ideal_chain:

            protein.matrix, protein.chain = get_matrix(best_chain)
            break

        # Adds amino to the protein chain.
        protein.chain.append(Amino(char, fold, amino_xy))

        print("Char " + str(len(protein.chain)) +"/" + str(len(protein.amino_string)) + ". Beste score: " + str(best_score))
        print("")

        # Pop the first char from the string. That one has been processed now
        chars = chars[1:]

        # Reset the best score and best chain
        best_score = 1
        best_chain = []

    # Update matrix and protein of the chain. Offset happens now.
    protein.matrix, protein.chain = get_matrix(protein.chain)
    print("score:" + str(get_score(protein.chain, protein.matrix, ch_score)) + "")

    for amino in protein.chain:
        print(amino, end="")

# The actual algo for selecting the fold the chain will make.
def fold_selector(chain, chars, max_lookahead, chain_length_goal, ch_score):

    # This is the recursive functions which does the depth search.
    find_best_chain(chain, chars, max_lookahead, ch_score)

    # IF the algo has actually found the FULL best chain , return the best chain.
    if len(best_chain) == chain_length_goal:
        print('found best chain.')
        return True, None

    # If the algo only found a partial best chain. returns only the next best move to take.
    if best_chain:
        return False, best_chain[len(chain)].fold


    raise Exception("Couldn't find best chain")

# The recursive function which accepts the variables: the current chain of aminos, and the string of the aminos it has yet to process.
def find_best_chain(current_chain, chars, max_lookahead, ch_score):


    # The first char has to be popped because it processed that char.
    global current_lookahead
    if not current_lookahead == 0:
        chars = chars[1:]

    # If there is only 1 char left we've arrived at the end of a chain.
    if len(chars) == 1 or current_lookahead == max_lookahead:


        # Add the last char to the amino chain.
        current_chain.append(Amino(chars[0], 0, current_chain[-1].get_fold_coordinates()))


        # Calculate the matrix (needed for the score.) and the score
        matrix, xy_offset = get_matrix_efficient(current_chain)
        score = get_score_efficient(current_chain, matrix, xy_offset, ch_score)

        global best_score
        global best_chain


        # IF this score is the best score, save this score + chain as a global.
        if score < best_score:
            best_score = score
            best_chain = copy.deepcopy(current_chain)


        # Abort that chain if it isnt the best score. remove amino we just added
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

            # Append the next amino and increase current lookahead
            current_lookahead += 1
            current_chain.append(Amino(chars[0], move, last_amino.get_fold_coordinates()))

            find_best_chain(current_chain, chars, max_lookahead, ch_score)

            # After the algo the lookahead should return to last value and the amino we just added should be removed again.
            current_lookahead -= 1
            del current_chain[-1]
