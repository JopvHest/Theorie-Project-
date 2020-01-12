import random
from classes.amino import Amino
from algorithms.helpers import get_matrix, get_score, get_matrix_efficient, get_score_efficient
import copy

best_score = 1
best_chain = None
current_lookahead = 0

def depth_search_lookahead(protein, max_lookahead):
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
            ideal_chain, fold = fold_selector(protein.chain, chars, max_lookahead, chain_length_goal)


        # Ideal chain is already found, replace chain with ideal chain and break loop.
        if ideal_chain:
            for amino in best_chain:
                print(amino)

            protein.matrix, protein.chain = get_matrix(best_chain)
            break

        # Adds amino to the protein chain.
        protein.chain.append(Amino(char, fold, amino_xy))

        print("current chain: ", end="")
        for amino in protein.chain:
            print(amino, end="")
        print("")
        
        # Pop the first char from the string. That one has been processed now
        chars = chars[1:]
        
        # Reset the best score and best chain
        best_score = 1
        best_chain = 0
    
    # Update matrix and protein of the chain. Offset happens now.
    protein.matrix, protein.chain = get_matrix(protein.chain)
    print("score:" + str(get_score(protein.chain, protein.matrix)))

    for amino in protein.chain:
        print(amino, end="")

# The actual algo for selecting the fold the chain will make.
def fold_selector(chain, chars, max_lookahead, chain_length_goal):

    # This is the recursive functions which does the depth search.
    find_best_chain(chain, chars, max_lookahead)

    # IF the algo has actually found the FULL best chain , return the best chain.
    if len(best_chain) == chain_length_goal:
        print('found best chain.')
        return True, None
    
    # If the algo only found a partial best chain. returns only the next best move to take.
    if best_chain:
        print("best move: " + str(best_chain[0].fold) + ", best_chain: ", end="")
        for amino in best_chain:
            print(amino, end="")
        print("")

        return False, best_chain[len(chain)].fold


    raise Exception("Couldn't find best chain")

# The recursive function which accepts the variables: the current chain of aminos, and the string of the aminos it has yet to process.
def find_best_chain(current_chain, chars, max_lookahead):
    
    
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
        score = get_score_efficient(current_chain, matrix, xy_offset)

        global best_score
        global best_chain
        
        
        # IF this score is the best score, save this score + chain as a global.
        if score < best_score:
            print("New best score: " + str(score))
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
            
            find_best_chain(current_chain, chars, max_lookahead)

            # After the algo the lookahead should return to last value and the amino we just added should be removed again.
            current_lookahead -= 1
            del current_chain[-1]


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
