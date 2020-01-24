

from classes.amino import Amino
from functions.GetMatrix import get_matrix
from functions.GetLegalMoves import get_legal_moves
from functions.GetScore import get_score
import copy
import random



def hill_climbing(protein, iterations):
    
    # We start with a straight protein, you could replace this with a search (random for example)
    build_straight_protein(protein)
    print("start protein:")
    for amino in protein.chain.chain_list:
            print(amino)

    # Save the score at every iteration (Not yet implemented)
    scores = []
    total_iterations = 0

    # The amount of turns the score hasnt improved.
    times_not_improved = 0
    times_not_improved_limit = 1000

    # The overal best score and chain is saved here
    best_score = 1
    best_chain = protein.chain.chain_list

    while total_iterations < iterations:

    # max_index = len(protein.amino_string) - 1

    # for index in range(1, max_index):

        # print(index)

        # pick random index for chain and that amino.
        max_index = len(protein.amino_string) - 1
        chosen_index = random.randint(1, max_index - 1)
        # print("chosen_index", end="")
        # print(chosen_index)
        chosen_amino = protein.chain.chain_list[chosen_index]
        chosen_amino_fold = chosen_amino.fold
        
        # Save old chain if the random move doesnt turn out to be legal
        old_chain = copy.deepcopy(protein.chain.chain_list)

        # Also pick random move and apply.
        moves = get_legal_moves(chosen_amino.coordinates, protein.chain.chain_list)
        # print("legal moves: ", end="")
        # print(moves)
        if chosen_amino_fold in moves:
            moves.remove(chosen_amino_fold)
            # print("move removes: ", end="")
            # print(chosen_amino_fold)
            # print(moves)
        

        if not moves:
            continue
        
        chosen_move = random.choice(moves)
        # print("chosen_move", end="")
        # print(chosen_move)
        chosen_amino.fold = chosen_move

        next_amino = protein.chain.chain_list[chosen_index + 1]

        if chosen_index == max_index - 1:
            # change coordinated last amino
            # print("no next")
            pass

        
        
        

        elif chosen_move == next_amino.fold or chosen_index + 2 >= max_index:
            # print("only next")
            next_amino.fold = chosen_amino_fold
            # chain is correct from here
        # print("check * -1")
        # print(chosen_move * -1)
        # print(chosen_amino_fold)
        elif chosen_move * -1 == chosen_amino_fold:
            # print("to difficult")
            protein.chain.chain_list = old_chain
            continue
            # to complicated continue


        # elif chosen_move * -1 == next_amino.fold:
        else:
            # print("else")
            next_amino.fold = chosen_amino_fold

            after_next_amino = protein.chain.chain_list[chosen_index + 2]


            after_next_amino.fold = chosen_move * -1

            # pull chain

            for i in range(chosen_index + 1, max_index - 2):
                amino_changed = old_chain[i]
                # print("index: " + str(i))
                # print("amino changed: ", end="")
                # print(amino_changed)
                amino_pulled = protein.chain.chain_list[i + 2]
                # print("amino_pulled: ", end="")
                # print(amino_pulled)

                amino_pulled.fold = amino_changed.fold
                # print(amino_pulled.atype)
                # print(amino_pulled.fold)
                # print("amino_pulled2: ", end="")
                # print(amino_pulled)


        last_amino = protein.chain.chain_list[-1]
        last_amino.fold = 0

        # else:
        #     print("error")
        #     protein.chain.chain_list = old_chain 
        #     continue
        # print("end protein:")
        # for amino in protein.chain.chain_list:
        #     print(amino)


        # Rebuild the chain/matrix.
        legal_chain = rebuild_chain(protein, chosen_index + 1)

        # Function returns False if it isnt a legal chain.
        # If illegal chain, load back old_chain
        if not legal_chain:
            protein.chain.chain_list = old_chain
            continue
        
        # protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)
        # protein.print_protein()
        # protein.chain.chain_list = old_chain

        total_iterations += 1
        print(str(total_iterations) + "/" + str(iterations))

        # Load matrix of new chain
        protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)

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
        
        old_amino.coordinates = new_coordinates
        index += 1
    
    return True
