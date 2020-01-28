# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.
# This file implements a beam search algorithm based on the breadth search algorithm.

import copy
from queue import Queue

from classes.amino import Amino
from classes.chain import Chain
from classes.protein import Protein
from functions.GetLegalMoves import get_legal_moves, get_legal_moves_nomirror
from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient
from functions.IsChain3d import check_dimensions


# This is a Breadth first search which discards chains with subpar scors at specific depths.
def beam_search(protein, ch_score, selection_levels):

    # Check if unsupported 3d mode.
    check_dimensions(protein.chain.chain_list)

    # Get chain WITH first amino already in it.
    start_chain = protein.chain

    # Create queue and put the first amino in it.
    queue = Queue(maxsize = 0)
    queue.put(start_chain)

    # Finished queues. Is this smart?
    finished_chains = []

    # Keeps track of scores in 1 layer.
    scores = []

    # Go trough the queue.
    while not queue.empty():
        # Get the first chain from the queue.
        chain_actual = queue.get()

        # Get the index from the length of the chain.
        index = len(chain_actual.chain_list)

        # Specifies if we are at a level before or at the level for selecting chains to abandon.
        saving_score = False
        selecting = False

        if index + 1 in selection_levels:
            saving_score = True
        elif index in selection_levels:
            cutoff_score = sum(scores)/len(scores)
            selecting = True
        elif index - 1 in selection_levels:
            scores = []

        # Remove chain from queue if score is worse than cutoff score.
        if selecting:
            chain_score = chain_actual.score
            if chain_score > cutoff_score:
                continue

        # Last amino always has fold of 0.
        if  index + 1 == len(protein.amino_string):

            fold = 0
            atype = protein.amino_string[index]
            coordinates = chain_actual.chain_list[-1].get_fold_coordinates()

            new_amino = Amino(atype, fold, coordinates)
            chain_actual.chain_list.append(new_amino)

            finished_chains.append(chain_actual)

        # Determine fold and make new chain for every possibility.
        else:
            legal_moves = get_legal_moves(chain_actual.chain_list[-1].get_fold_coordinates(), chain_actual.chain_list)

            # If there are no legal moves chain ends here.
            if legal_moves:
                # Go trough the legal moves and make a new_chain for every move, then put them in the queue.
                for move in legal_moves:
                    atype = protein.amino_string[index]
                    coordinates = chain_actual.chain_list[-1].get_fold_coordinates()

                    # Make a new amino and add it to the a new chain with deepcopy.
                    amino = Amino(atype, move, coordinates)
                    new_chain = copy.deepcopy(chain_actual)
                    new_chain.chain_list.append(amino)

                    # Put the new chain in the queue.
                    if not saving_score:
                        queue.put(new_chain)
                    # If saving score, set chain's score variable to its score, and add score to this layer's score list.
                    else:
                        matrix, offset = get_matrix_efficient(new_chain.chain_list)
                        score = get_score_efficient(new_chain.chain_list, matrix, offset, 1)
                        new_chain.score = score

                        queue.put(new_chain)
                        scores.append(score)

    # The best score and corresponding chain that has been found.
    best_score = 1
    best_chains = []

    # Goes over all finished chains to find the one with the best score.
    for chain in finished_chains:
        protein1 = Protein(protein.amino_string, "2d")
        protein1.matrix, protein1.chain = get_matrix(copy.deepcopy(chain).chain_list)

        matrix, xy_offset = get_matrix_efficient(chain.chain_list)
        score = get_score_efficient(chain.chain_list, matrix, xy_offset, ch_score)

        # If the score is better than the best score, replace best_chains.
        # If score is equal add chain to best_chains.
        if score < best_score:
            best_score = score
            best_chains = []
            print("New best score: " + str(score))
            best_chains.append(chain)
        elif score == best_score:
            best_chains.append(chain)
    
    protein.matrix, protein.chain.chain_list = get_matrix(best_chains[0].chain_list)
