# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.
# This file implements an iterative algorithm which randomly refolds 1 fold.
# It lowers the chance to accept folds which do not improve the score when "temperature" drops.

import copy
import random

from algorithms.DepthSearchLookahead import depth_search_lookahead
from classes.amino import Amino
from functions.GetLegalMoves import get_legal_moves
from functions.GetMatrix import get_matrix
from functions.GetScore import get_score

# This functions tries to find a best protein by using simulated annealing
def hill_climbing_annealing(protein, iterations):
    # We start with a straight protein, you could replace this with a search (random for example)
    build_straight_protein(protein)

    # Save the score at every iteration (Not yet implemented)
    scores = []
    total_iterations = 0

    # The overal best score and chain is saved here
    best_score = 0
    best_chain = []

    temperature_start =  5
    temperature_end = 0.5
    temp_step = (temperature_start - temperature_end) / iterations
    temperature = temperature_start

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
        
        # Rebuild chain for that point on.
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

        # New best score
        if score < best_score:
            print("new best score: ", end="")
            print(score)
            best_score = score
            best_chain = copy.deepcopy(protein.chain.chain_list)

        # Calculate if chain should be accepted based on:
        # New score, old score, temperature, random number
        acceptance_rate = (2**(abs(score) - abs(protein.chain.score))) / temperature
        random_number = random.uniform(0, 1)

        # Accept iteration
        if random_number < acceptance_rate:
            protein.chain.score = score
        
        # Abbandon iteration
        else:
            protein.chain.chain_list = old_chain
        
        temperature =  temperature - temp_step
    
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

    # Get all coordinates before the amino with the new fold
    while index < index_to_start_from:
        coordinates_list.append(protein.chain.chain_list[index].coordinates)
        index += 1

    # Give all aminos after the amino with the new fold new coordinates.
    # If one of these coordinates already exist, chain is illegal.
    while index < len(protein.amino_string):
        old_amino = protein.chain.chain_list[index]
        new_coordinates = protein.chain.chain_list[index - 1].get_fold_coordinates()
        
        if new_coordinates in coordinates_list:
            return False
        
        old_amino.coordinates = new_coordinates
        index += 1
    
    return True
