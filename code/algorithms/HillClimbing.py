# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.
# This file implements an iterative algorithm which randomly refolds 1 fold and checks if this improves the score.

import copy
import random

from classes.amino import Amino
from functions.GetLegalMoves import get_legal_moves
from functions.GetMatrix import get_matrix
from functions.GetScore import get_score
from functions.IterativeFunctions import rebuild_chain, build_straight_protein



# This search tries to find a best protein by using Hill climbing
def hill_climbing(protein, iterations, max_non_improvements):
    
    # We start with a straight protein, you could replace this with a search (random for example)
    build_straight_protein(protein)

    # Save the score at every iteration (Not yet implemented)
    scores = []
    total_iterations = 0

    # The amount of turns the score hasnt improved.
    times_not_improved = 0
    times_not_improved_limit = max_non_improvements

    # The overal best score and chain is saved here
    best_score = 0
    best_chain = []

    while total_iterations < iterations:

        # pick random index for chain and that amino.
        chosen_index = random.randint(0, len(protein.amino_string) - 1)
        chosen_amino = protein.chain.chain_list[chosen_index]
        
        # Save old chain if the random move doesnt turn out to be legal
        old_chain = copy.deepcopy(protein.chain.chain_list)

        # Also pick random move and apply.
        moves = get_legal_moves(chosen_amino.coordinates, protein.chain.chain_list)
        
        if not moves:
            continue
        
        chosen_move = random.choice(moves)
        chosen_amino.fold = chosen_move
        
        # Rebuild the chain/matrix.
        legal_chain = rebuild_chain(protein, chosen_index + 1)

        # Function returns False if it isnt a legal chain.
        # If illegal chain, load back old_chain
        if not legal_chain:
            protein.chain.chain_list = old_chain

        total_iterations += 1

        # Load matrix of new chain
        protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)

        # Calculate score of new chain
        score = get_score(protein.chain.chain_list, protein.matrix)
        
        # Continue with new chain if same or better score
        if score <= protein.chain.score:
            # New "local" best score
            if score < protein.chain.score:
                # Reset times not improved
                times_not_improved = 0

                # Actual new best score
                if score < best_score:
                    print("new best score: ", end="")
                    print(score)
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