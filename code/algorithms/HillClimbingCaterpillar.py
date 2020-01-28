# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.
# This file implements an iterative algorithm which randomly refolds 1-3 folds.

import copy
import random

from classes.amino import Amino
from functions.GetLegalMoves import get_legal_moves
from functions.GetMatrix import get_matrix
from functions.GetScore import get_score
from functions.IsChain3d import check_dimensions

# iterative algorithm which selects a random amino and reforlds 1-3 folds from there
def hill_climbing_caterpillar(protein, iterations, max_non_improvements):
    
    # Check if unsupported 3d mode.
    check_dimensions(protein.chain.chain_list)

    # We start with a straight protein, you could replace this with a search (random for example)
    build_straight_protein(protein)
    
    # take count of the number of iterations
    total_iterations = 0

    # The amount of turns the score hasnt improved.
    times_not_improved = 0
    times_not_improved_limit = max_non_improvements

    # The overal best score and chain is saved here
    best_score = 1
    best_chain = protein.chain.chain_list

    while total_iterations < iterations:

        # pick random index for chain and that amino.
        max_index = len(protein.amino_string) - 1
        chosen_index = random.randint(1, max_index - 1)
        
        # get the amino and his fold with the random index
        chosen_amino = protein.chain.chain_list[chosen_index]
        chosen_amino_fold = chosen_amino.fold
        
        # Save old chain if the random move doesnt turn out to be legal
        old_chain = copy.deepcopy(protein.chain.chain_list)

        # Also pick random move and apply.
        moves = get_legal_moves(chosen_amino.coordinates, protein.chain.chain_list)
       
        # remove initial move from the moves
        if chosen_amino_fold in moves:
            moves.remove(chosen_amino_fold)
        
        # if there a no possible new moves for this amino loop again
        if not moves:
            continue
        
        # choose random fold and adjust fold of amino
        chosen_move = random.choice(moves)
        chosen_amino.fold = chosen_move

        # get the amino thereafter from the chain
        next_amino = protein.chain.chain_list[chosen_index + 1]

        # If the chosen amino is the one before the last only this amino needed to change
        if chosen_index == max_index - 1:
            pass
        
        # if the there need to be changed only 2 aminos
        elif chosen_move == next_amino.fold or chosen_index + 2 >= max_index:
            next_amino.fold = chosen_amino_fold

        # skip if new move is 180 degrees to the other side, rearanging gets very difficult  
        elif chosen_move * -1 == chosen_amino_fold:
            protein.chain.chain_list = old_chain
            continue
            
        else:
            # change next fold and the fold after that
            next_amino.fold = chosen_amino_fold
            after_next_amino = protein.chain.chain_list[chosen_index + 2]
            after_next_amino.fold = chosen_move * -1

            # pull rest of the chain by changing position of aminos thereafter 2 places
            for i in range(chosen_index + 1, max_index - 2):
                amino_changed = old_chain[i] 
                amino_pulled = protein.chain.chain_list[i + 2]
                amino_pulled.fold = amino_changed.fold
                

        # Make sure last amino gets a fold of 0
        last_amino = protein.chain.chain_list[-1]
        last_amino.fold = 0

        # Rebuild the chain/matrix.
        legal_chain = rebuild_chain(protein, chosen_index + 1)

        # Function returns False if it isnt a legal chain.
        # If illegal chain, load back old_chain
        if not legal_chain:
            protein.chain.chain_list = old_chain
            continue

        total_iterations += 1

        # to check the progress by printing
        if total_iterations % 1000 == 0:
            print(str(total_iterations) + "/" + str(iterations))

        # Load matrix of new chain
        protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)

        # check for errror and revert to old chain
        if protein.chain.chain_list == False:
            protein.chain.chain_list = old_chain
            print("error: false chain")
            continue

        # Calculate score of new chain
        score = get_score(protein.chain.chain_list, protein.matrix)
      
        
        # Continue with new chain if same or better score
        if score <= protein.chain.score:
            # New "local" best score
            if score < protein.chain.score:
                print("new best score: ", end="")
                print(score)
                # Reset times not improved
                times_not_improved = 0

                # Actual new best score
                if score < best_score:
                    best_score = score
                    best_chain = copy.deepcopy(protein.chain.chain_list)

            # Score is same so not improved.
            else:
                times_not_improved += 1

            protein.chain.score = score
        
        # Chain is worse
        else:
            
            # If times not improved limit is reaced, continue with that chain anyway
            if times_not_improved >= times_not_improved_limit:
                protein.chain.score = score
                times_not_improved = 0
            
            # abandon that chain.
            else:
                protein.chain.chain_list = old_chain
    
    # Save the best score and chain in the protein
    protein.chain.chain_list = best_chain
    protein.matrix, protein.chain.chain_list = get_matrix(best_chain)


# This function builds a straight protein which only has folds of 2 (up)
def build_straight_protein(protein):
    mode_3d = protein.mode_3d

    if mode_3d:
        protein.chain.chain_list[0].coordinates = [0, 0, 0]


    else:
        protein.chain.chain_list[0].coordinates = [0, 0]
    
    
    for index, char in enumerate(protein.amino_string):
        if index == 0:
            continue
        
        new_amino = Amino(char, 2, protein.chain.chain_list[index - 1].get_fold_coordinates())


        protein.chain.chain_list.append(new_amino)

    protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)

# Rebuilds chain with 1 new fold, returns False if illegal chain
def rebuild_chain(protein, index_to_start_from):

    index = 0
    coordinates_list = []

    while index < index_to_start_from:
        coordinates_list.append(protein.chain.chain_list[index].coordinates)
        index += 1

    while index < len(protein.amino_string):
        old_amino = protein.chain.chain_list[index]
        new_coordinates = protein.chain.chain_list[index - 1].get_fold_coordinates()
        
        if new_coordinates in coordinates_list:
            return False
        
        coordinates_list.append(new_coordinates)
        
        old_amino.coordinates = new_coordinates
        index += 1
    
    return True
