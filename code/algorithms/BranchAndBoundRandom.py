# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.
# This file implements.

import copy
import random

from classes.amino import Amino
from classes.chain import Chain
from functions.GetLegalMoves import get_legal_moves, get_legal_moves_nomirror
from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient, get_score, get_score_iterative, get_score_iterative_and_spots
from functions.IsChain3d import is_chain_3d
from functions.MinChainLenNeeded import chain_can_reach_spot
from functions.IsChain3d import check_dimensions

best_score = 1
best_chain = None
best_matrix = None


# The chance a chain gets rejected if its score is under the average for that depth.
p_below_average = 0

# The chance a chain gets rejected if its score is above the average for that depth.
p_above_average = 0

# This saves the best score, average score, and amount of chains used for that avg at the index of the depth.
# So at a depth of 6: partial_energies[6] = best_score, average_score, amount of chains tp calculate that average
partial_energies = []

# This is a version of the branch and bound random which randomsly throws away chains based on average score on a depth.
def branch_and_bound_random(protein, ch_score, best_score_import, p1, p2):
    global best_score
    global p_below_average
    global p_above_average
    p_below_average = p1
    p_above_average = p2

    # Check if unsupported 3d mode.
    check_dimensions(protein.chain.chain_list)

    # You could import a score to start at (if you know the score to be at least that amount).
    best_score = best_score_import
    
    char_counter = 1

    mode_3d = protein.mode_3d
    
    # Build up the partial energy list for every depth in the chain.
    global partial_energies
    partial_energies.append([])
    for char in protein.amino_string:
        partial_energies.append([0, 0, 0])


    if mode_3d:
        # Build a matrix with dimensions of 2 * length of the protein + 1.
        matrix_dimensions = 2 * len(protein.amino_string) + 1
        
        for k in range(matrix_dimensions + 1):
            layer = []
            for i in range(matrix_dimensions + 1):
                row = []
                for j in range(matrix_dimensions + 1):
                    row.append(" ")
                layer.append(row)
            protein.chain.matrix.append(layer)
        print(len(protein.chain.matrix), len(protein.chain.matrix[1]), len(protein.chain.matrix[1][1]))
        protein.chain.chain_list[0].coordinates = [len(protein.amino_string) + 1 , len(protein.amino_string) + 1, len(protein.amino_string) + 1]
        protein.chain.matrix[len(protein.amino_string) + 1][len(protein.amino_string) + 1][len(protein.amino_string) + 1] = protein.chain.chain_list[0]

    # 2D
    else:
        # Build a matrix with dimensions of 2 * length of the protein +1.
        matrix_dimensions = 2 * len(protein.amino_string) + 1
        for i in range(matrix_dimensions + 1):
            row = []
            for j in range(matrix_dimensions + 1):
                row.append(" ")
            protein.chain.matrix.append(row)
        
        # Center the first amino's coordinates in the matrix and add it to the matrix.
        protein.chain.chain_list[0].coordinates = [len(protein.amino_string) + 1 , len(protein.amino_string) + 1]
        protein.chain.matrix[len(protein.amino_string) + 1][len(protein.amino_string) + 1] = protein.chain.chain_list[0]

    # Perform all functions to add corrent spots.
    new_score, spots_to_add, spots_to_remove, spots_to_add_C, spots_to_remove_C = get_score_iterative_and_spots(protein.chain, protein.chain.matrix, 0)
    protein.chain.add_fold_spots(spots_to_add, "H")
    protein.chain.remove_fold_spots(spots_to_remove, "H")
    protein.chain.add_fold_spots(spots_to_add_C, "C")
    protein.chain.remove_fold_spots(spots_to_remove_C, "C")
        

    # Skips the first char the index.
    while protein.char_counter < len(protein.amino_string):

        char = protein.amino_string[protein.char_counter]
        # Get the location the last amino folded to.
        # Note: an index of -1 gets the last object in a list.
        amino_xy = protein.chain.chain_list[-1].get_fold_coordinates()


        # Last amino always has fold of 0.
        if protein.char_counter + 1 == len(protein.amino_string):
            fold = 0

        # Determine which fold to pick.
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

    # The first char has to be popped because it processes that char in the last loop.
    # Note: popping the first loop is also valid because the first char is build before loading the fold_selector.
    chars = chars[1:]

    mode_3d = is_chain_3d(current_chain.chain_list)

    # If there is only 1 char left we've arrived at the end of a chain.
    if len(chars) == 1:
        # Add the last char to the amino chain AND the recusrive chain matrix
        last_amino = current_chain.chain_list[-1]
        coordinates = last_amino.get_fold_coordinates()
        new_amino = Amino(chars[0], 0, coordinates)
        current_chain.chain_list.append(new_amino)
        
        if mode_3d:
            current_chain.matrix[coordinates[2]][coordinates[1]][coordinates[0]] = new_amino
        else:
            current_chain.matrix[coordinates[1]][coordinates[0]] = new_amino
        
        new_score = get_score_iterative(current_chain.chain_list, current_chain.matrix, current_score)

        # Calculate the matrix (needed for the score.) and the score.
        score = new_score

        global best_chain


        # IF this score is the best score, save this score + chain as a global.
        if score < best_score:
            print("New best score: " + str(score))
            best_score = score
            best_chain = copy.deepcopy(current_chain.chain_list)


        # Abort that chain if it isnt the best score. also remove it from the matrix.
        if mode_3d:
            current_chain.matrix[coordinates[2]][coordinates[1]][coordinates[0]] = " "
        else:
            current_chain.matrix[coordinates[1]][coordinates[0]] = " "

        del current_chain.chain_list[-1]
        return None

    # Get legal moves on the position of that amino.
    legal_moves = get_legal_moves_nomirror(current_chain.chain_list[-1].get_fold_coordinates(), current_chain)


    # If no legals move left, abort the chain. The protein got "stuck".
    if not legal_moves:
        return None

    # Go recursively through all legal moves and its child legal moves etc.
    else:
        for move in legal_moves:

            # Find best chain needs a new updated chain, but the old chain also needs to be remembered.
            last_amino = current_chain.chain_list[-1]
            coordinates = last_amino.get_fold_coordinates()
            new_amino = Amino(chars[0], move, coordinates)
            current_chain.chain_list.append(new_amino)

            
            skip_function = False

            # Also add that amino to the matrix, and update the mirror status.
            if mode_3d:
                current_chain.matrix[coordinates[2]][coordinates[1]][coordinates[0]] = new_amino
            else:
                current_chain.matrix[coordinates[1]][coordinates[0]] = new_amino

            current_chain.update_mirror_status()
            
            # Calculate new score and and/remove the correct fold spots.
            new_score, spots_to_add, spots_to_remove, spots_to_add_C, spots_to_remove_C = get_score_iterative_and_spots(current_chain, current_chain.matrix, current_score)
            
            
            # Remove the spots that are now filled by aminos.
            current_chain.remove_fold_spots(spots_to_remove, "H")
            current_chain.remove_fold_spots(spots_to_remove_C, "C")

            # Change odd/even.
            current_chain.odd = not current_chain.odd
            
            # Add the spots that were newly created.
            current_chain.add_fold_spots(spots_to_add, "H")
            current_chain.add_fold_spots(spots_to_add_C, "C")

            

            
            # Calculate max extra score and prune spots that are too far away.
            extra_score_possible, removed_even, removed_odd, removed_even_C, removed_odd_C = current_chain.get_max_possible_extra_score(chars[1:])
            max_possible = new_score + extra_score_possible
            
            # Of a new best score cant be reached, abandon chain.
            if max_possible >= best_score:

                skip_function = True
            
            global partial_energies
            current_depth = len(current_chain.chain_list)
            
            # If it is the new best score for that depth.
            if new_score <= partial_energies[current_depth][0]:
                if new_score < partial_energies[current_depth][0]:
                    partial_energies[current_depth][0] = new_score
                
                partial_energies[current_depth][1] = calculate_average(partial_energies[current_depth][1], partial_energies[current_depth][2], new_score)
                partial_energies[current_depth][2] += 1
            
            # The score is below average (so better) for that depth.
            elif new_score <= partial_energies[current_depth][1]:
                global p_below_average
                random_number = random.uniform(0, 1)

                if random_number > p_below_average:
                    skip_function = True
                
                else:
                    partial_energies[current_depth][1] = calculate_average(partial_energies[current_depth][1], partial_energies[current_depth][2], new_score)
                    partial_energies[current_depth][2] += 1

            # The score is above average (so worse) for that depth.
            else:
                global p_above_average
                random_number = random.uniform(0, 1)

                if random_number > p_above_average:
                    skip_function = True
                
                else:
                    partial_energies[current_depth][1] = calculate_average(partial_energies[current_depth][1], partial_energies[current_depth][2], new_score)
                    partial_energies[current_depth][2] += 1

            if not skip_function:
                # The actual recursive function.
                find_best_chain(current_chain, chars, ch_score, new_score)

            # Undo all the changed to the spots that were made before calling the recursive function.
            current_chain.add_back_even(removed_even, "H")
            current_chain.add_back_odd(removed_odd, "H")
            current_chain.add_back_even(removed_even_C, "C")
            current_chain.add_back_odd(removed_odd_C, "C")
            current_chain.remove_fold_spots(spots_to_add, "H")
            current_chain.remove_fold_spots(spots_to_add_C, "C")

            
            # Change odd/even back.
            current_chain.odd = not current_chain.odd

            # Reverse the fold spots.
            current_chain.add_fold_spots(spots_to_remove, "H")
            current_chain.add_fold_spots(spots_to_remove_C, "C")

            # Reverse the matrix and mirror status.
            if mode_3d:
                current_chain.matrix[coordinates[2]][coordinates[1]][coordinates[0]]
            else:
                current_chain.matrix[coordinates[1]][coordinates[0]] = " "
            current_chain.update_mirror_status_reverse()
            
            # Undo the added amino.
            del current_chain.chain_list[-1]

# This functions calculates a new average based on the average, the amount of entries used to calculate this average, and a new enrty.
def calculate_average(average, average_amount, new_entry):

    # Maths..
    new_average = ( average * (average_amount)/(average_amount + 1)) + (new_entry * 1 / (average_amount + 1))
    
    return new_average