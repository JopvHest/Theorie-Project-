import random
from classes.amino import Amino
from classes.chain import Chain
from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient, get_score, get_score_iterative
from functions.GetLegalMoves import get_legal_moves, get_legal_moves_nomirror
import copy

best_score = 1
best_chain = None
best_matrix = None

#depth_score_dict = {
#    "1" : [[average_score, amount_of_scores], [best_score]]
#   "2" : [[average_score, amount_of_scores], [best_score]]
#}

def depth_search_iterative(protein, ch_score):
    char_counter = 1

    # Build a matrix with dimensions of 2 * length of the protein +1
    matrix_dimensions = 2 * len(protein.amino_string) + 1
    for i in range(matrix_dimensions + 1):
        row = []
        for j in range(matrix_dimensions + 1):
            row.append(" ")
        protein.chain.matrix.append(row)
    
    # Center the first amino's coordinates in the matrix and add it to the matrix.
    protein.chain.chain_list[0].coordinates = [len(protein.amino_string) + 1 , len(protein.amino_string) + 1]
    protein.chain.matrix[len(protein.amino_string) + 1][len(protein.amino_string) + 1] = protein.chain.chain_list[0]
        

    # Skips the first char the index.
    while protein.char_counter < len(protein.amino_string):

        # print(str(self.char_counter))
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
            ideal_chain = fold_selector(amino_xy, char, protein.chain, illegal_folds, protein.amino_string, ch_score)


        # Ideal chain is already found, replace chain with ideal chain and break loop.
        if ideal_chain:
            for amino in best_chain:
                print(amino)

            protein.matrix, protein.chain.chain_list = get_matrix(best_chain)
            break


        # Adds amino to the protein chain.
        protein.chain.chain_list.append(Amino(char, fold, amino_xy))
        char_counter += 1



# The actual algo for selecting the fold the chain will make.
def fold_selector(xy, char, chain, illegal_moves, chars, ch_score):

    # This is the recursive functions which does the depth search.
    find_best_chain(chain, chars, ch_score, 0)

    # IF the algo has actually found the best chain (which it should), return the best chain.
    if best_chain:
        return (True)


    raise Exception("Couldn't find best chain")

# The recursive function which accepts the variables: the current chain of aminos, and the string of the aminos it has yet to process.
def find_best_chain(current_chain, chars, ch_score, current_score):

    global best_score
    
    # The first char has to be popped because it processes that char in the last loop
    # Note: popping the first loop is also valid because the first char is build before loading the fold_selector.
    chars = chars[1:]

    # If there is only 1 char left we've arrived at the end of a chain.
    if len(chars) == 1:

        # Add the last char to the amino chain AND the recusrive chain matrix
        last_amino = current_chain.chain_list[-1]
        new_amino_x, new_amino_y = last_amino.get_fold_coordinates()
        new_amino = Amino(chars[0], 0, [new_amino_x, new_amino_y])
        current_chain.chain_list.append(new_amino)
        current_chain.matrix[new_amino_y][new_amino_x] = new_amino
        
        new_score = get_score_iterative(current_chain.chain_list, current_chain.matrix, current_score)

        # Calculate the matrix (needed for the score.) and the score
        score = new_score

        global best_score
        global best_chain


        # IF this score is the best score, save this score + chain as a global.
        if score < best_score:
            print("New best score: " + str(score))
            best_score = score
            best_chain = copy.deepcopy(current_chain.chain_list)


        # Abort that chain if it isnt the best score. also remove it from the matrix
        current_chain.matrix[new_amino_y][new_amino_x] = " "
        del current_chain.chain_list[-1]
        return None

    # Get legal moves on the position of that amino
    legal_moves = get_legal_moves_nomirror(current_chain.chain_list[-1].get_fold_coordinates(), current_chain)


    # If no legals move left, abort the chain. The protein got "stuck"
    if not legal_moves:
        return None

    # Go recursively through all legal moves and its child legal moves etc.
    else:
        for move in legal_moves:

            # Find best chain needs a new updated chain, but the old chain also needs to be remembered.
            last_amino = current_chain.chain_list[-1]
            new_amino_x, new_amino_y = last_amino.get_fold_coordinates()
            new_amino = Amino(chars[0], move, [new_amino_x, new_amino_y])
            current_chain.chain_list.append(new_amino)

            # Also add that amino to the matrix, and update the mirror starus
            current_chain.matrix[new_amino_y][new_amino_x] = new_amino
            current_chain.update_mirror_status()
            
            # Calculate new score 
            new_score = get_score_iterative(current_chain.chain_list, current_chain.matrix, current_score)

            find_best_chain(current_chain, chars, ch_score, new_score)

            # Reverse the matrix and mirror status
            current_chain.matrix[new_amino_y][new_amino_x] = " "
            current_chain.update_mirror_status_reverse()
            

            del current_chain.chain_list[-1]