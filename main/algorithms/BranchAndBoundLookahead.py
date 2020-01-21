import random
from classes.amino import Amino
from classes.chain import Chain
from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient, get_score, get_score_iterative
from functions.GetLegalMoves import get_legal_moves, get_legal_moves_nomirror
from functions.MinChainLenNeeded import chain_can_reach_spot
from functions.GetScore import get_score_iterative_and_spots
import copy

best_score = 1
best_chain = []
best_matrix = None
current_lookahead = 0

#depth_score_dict = {
#    "1" : [[average_score, amount_of_scores], [best_score]]
#   "2" : [[average_score, amount_of_scores], [best_score]]
#}

def branch_and_bound_lookahead(protein, ch_score, best_score_import, max_lookahead):
    global best_score
    global best_chain
    best_score = best_score_import
    

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

    new_score, spots_to_add, spots_to_remove, spots_to_add_C, spots_to_remove_C = get_score_iterative_and_spots(protein.chain, protein.chain.matrix, 0)
    protein.chain.add_fold_spots(spots_to_add, "H")
    protein.chain.remove_fold_spots(spots_to_remove, "H")
    protein.chain.add_fold_spots(spots_to_add_C, "C")
    protein.chain.remove_fold_spots(spots_to_remove_C, "C")
    
    current_score = 0
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
            ideal_chain, fold = fold_selector(amino_xy, char, protein.chain, protein.amino_string[protein.char_counter - 1:], ch_score, max_lookahead, current_score)


        # Ideal chain is already found, replace chain with ideal chain and break loop.
        if ideal_chain:
            for amino in best_chain:
                print(amino)

            protein.matrix, protein.chain.chain_list = get_matrix(best_chain)
            break

        new_amino = Amino(char, fold, amino_xy)
        # Adds amino to the protein chain.
        protein.chain.chain_list.append(new_amino)
        
        # Also add that amino to the matrix, and update the mirror starus
        protein.chain.matrix[amino_xy[0]][amino_xy[1]] = new_amino
   
        
        # Calculate new score and and/remove the correct fold spots
        new_score, spots_to_add, spots_to_remove, spots_to_add_C, spots_to_remove_C = get_score_iterative_and_spots(protein.chain, protein.chain.matrix, current_score)
        
        current_score = new_score
        print(spots_to_add, spots_to_add_C)
        
        # Remove the spots that are now filled by aminos.
        protein.chain.remove_fold_spots(spots_to_remove, "H")
        protein.chain.remove_fold_spots(spots_to_remove_C, "C")

        # Change odd/even
        protein.chain.odd = not protein.chain.odd
        
        # Add the spots that were newly created.
        spots_to_add.append(protein.chain.chain_list[-1].get_fold_coordinates())
        protein.chain.add_fold_spots(spots_to_add, "H")
        protein.chain.add_fold_spots(spots_to_add_C, "C")
        protein.chain.get_max_possible_extra_score(protein.amino_string[protein.char_counter:])


        protein.char_counter += 1

        for amino in protein.chain.chain_list:
            print(amino, end='')
        print()


        best_chain = []
        best_score = 1
        
        print(protein.chain.available_bonds_odd_H)
        print(protein.chain.available_bonds_odd_C)
        print(protein.chain.available_bonds_even_H)
        print(protein.chain.available_bonds_even_C)


    
    protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)



# The actual algo for selecting the fold the chain will make.
def fold_selector(xy, char, chain, chars, ch_score, max_lookahead, current_score):

    # This is the recursive functions which does the depth search.
    find_best_chain(chain, chars, ch_score, 0, max_lookahead)

    # IF the algo has actually found the best chain (which it should), return the best chain.
    if len(best_chain) == len(chars):
        print('found best chain.')
        return True, None

    # If the algo only found a partial best chain. returns only the next best move to take.
    if best_chain:
        return False, best_chain[len(chain.chain_list)].fold

    raise Exception("Couldn't find best chain")

# The recursive function which accepts the variables: the current chain of aminos, and the string of the aminos it has yet to process.
def find_best_chain(current_chain, chars, ch_score, current_score, max_lookahead):


    global best_score
    global current_lookahead
    

    # The first char has to be popped because it processes that char in the last loop
    # Note: popping the first loop is also valid because the first char is build before loading the fold_selector.
    chars = chars[1:]

    # If there is only 1 char left we've arrived at the end of a chain.
    if len(chars) == 1 or current_lookahead == max_lookahead:
        # Add the last char to the amino chain AND the recusrive chain matrix
        last_amino = current_chain.chain_list[-1]
        new_amino_x, new_amino_y = last_amino.get_fold_coordinates()
        new_amino = Amino(chars[0], 0, [new_amino_x, new_amino_y])
        current_chain.chain_list.append(new_amino)
        current_chain.matrix[new_amino_y][new_amino_x] = new_amino
        
        new_score = get_score_iterative(current_chain.chain_list, current_chain.matrix, current_score)

        # Calculate the matrix (needed for the score.) and the score
        score = new_score

        global best_chain


        # IF this score is the best score, save this score + chain as a global.
        if score < best_score:
            print("New best score: " + str(score))
            best_score = score
            best_chain = copy.deepcopy(current_chain.chain_list)
            for amino in current_chain.chain_list:
                print(amino, end='')
            print()


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
            # for amino in current_chain.chain_list:
            #     print(amino, end="")
            # print()
            
            # print(str(current_chain.available_bonds_even_H), str(current_chain.available_bonds_odd_H))
            # Find best chain needs a new updated chain, but the old chain also needs to be remembered.
            last_amino = current_chain.chain_list[-1]
            new_amino_x, new_amino_y = last_amino.get_fold_coordinates()
            new_amino = Amino(chars[0], move, [new_amino_x, new_amino_y])
            current_chain.chain_list.append(new_amino)

            current_lookahead += 1

            
            

            # Also add that amino to the matrix, and update the mirror starus
            current_chain.matrix[new_amino_y][new_amino_x] = new_amino
            current_chain.update_mirror_status()
            
            # Calculate new score and and/remove the correct fold spots
            new_score, spots_to_add, spots_to_remove, spots_to_add_C, spots_to_remove_C = get_score_iterative_and_spots(current_chain, current_chain.matrix, current_score)

            # Remove the spots that are now filled by aminos.
            current_chain.remove_fold_spots(spots_to_remove, "H")
            current_chain.remove_fold_spots(spots_to_remove_C, "C")

            # Change odd/even
            current_chain.odd = not current_chain.odd
            
            # Add the spots that were newly created.
            current_chain.add_fold_spots(spots_to_add, "H")
            current_chain.add_fold_spots(spots_to_add_C, "C")

            

            
            # Calculate max extra score and prune spots that are too far away.
            extra_score_possible, removed_even, removed_odd, removed_even_C, removed_odd_C = current_chain.get_max_possible_extra_score(chars[1:])
            max_possible = new_score + extra_score_possible
            
            # Of a new best score cant be reached, abandon chain.
            if max_possible >= best_score:

                # Undo all the changes that were made to the spots.
                current_chain.add_back_even(removed_even, "H")
                current_chain.add_back_odd(removed_odd, "H")
                current_chain.add_back_even(removed_even_C, "C")
                current_chain.add_back_odd(removed_odd_C, "C")
                current_chain.remove_fold_spots(spots_to_add, "H")
                current_chain.remove_fold_spots(spots_to_add_C, "C")

                
                # Change odd/even back
                current_chain.odd = not current_chain.odd

                # Reverse the fold spots
                current_chain.add_fold_spots(spots_to_remove, "H")
                current_chain.add_fold_spots(spots_to_remove_C, "C")

                # Reverse the matrix and mirror status
                current_chain.matrix[new_amino_y][new_amino_x] = " "
                current_chain.update_mirror_status_reverse()
                
                # Remove the last amino
                del current_chain.chain_list[-1]
                continue

            # print(str(new_score) + " + " + str(extra_score_possible) + " = " + str(max_possible))
            
          
            # print("max possible score: " + str(extra_score_possible + new_score))
            # print(str(removed_even), str(removed_odd))
            # print(new_score)
            # print()

            # The actual recursive function
            find_best_chain(current_chain, chars, ch_score, new_score, max_lookahead)

            # Undo all the changed to the spots that were made before calling the recursive function.
            current_chain.add_back_even(removed_even, "H")
            current_chain.add_back_odd(removed_odd, "H")
            current_chain.add_back_even(removed_even_C, "C")
            current_chain.add_back_odd(removed_odd_C, "C")
            current_chain.remove_fold_spots(spots_to_add, "H")
            current_chain.remove_fold_spots(spots_to_add_C, "C")

            
            # Change odd/even back
            current_chain.odd = not current_chain.odd

            # Reverse the fold spots
            current_chain.add_fold_spots(spots_to_remove, "H")
            current_chain.add_fold_spots(spots_to_remove_C, "C")

            # Reverse the matrix and mirror status
            current_chain.matrix[new_amino_y][new_amino_x] = " "
            current_chain.update_mirror_status_reverse()
            
            current_lookahead -= 1
            del current_chain.chain_list[-1]