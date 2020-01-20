# pseudocode

# stack = list with all current chains.
# Only has 1 chain at the start. a chain with the start move.

# While True:
#   for chain in stack:
#       remove chain from stack
#       for move in legal_moves(chain):
#           add chain+move to the chain. At the place of the original chain (That got removed)
# When every chain in the stack arrived at the end of the amino_string. Compare the scores of ALL chains.

# For beam search we compare all the chains every x turns and remove the worst x procent.


from classes.amino import Amino
from classes.chain import Chain

from queue import Queue
import copy
from classes.protein import Protein
from classes.chain import Chain


from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient
from functions.GetLegalMoves import get_legal_moves, get_legal_moves_nomirror


def breadth_search(protein, ch_score):

    # Get chain WITH first amino already in it.
    start_chain = protein.chain
    # Create queue and put the first amino in it
    queue = Queue(maxsize = 0)
    queue.put(start_chain)

    # Finished queues. Is this smart?
    finished_chains = []

    # Go trough the queue
    while not queue.empty():
        # Get the first chain from the queue
        chain_actual = queue.get()

        # Get the index from the length of the chain
        index = len(chain_actual.chain_list)

        # Last amino always has fold of 0.
        if  index + 1 == len(protein.amino_string):

            fold = 0
            atype = protein.amino_string[index]
            coordinates = chain_actual.chain_list[-1].get_fold_coordinates()
            new_amino = Amino(atype, fold, coordinates)
            chain_actual.chain_list.append(new_amino)

            # Save the chain to the finished chain list.
            finished_chains.append(chain_actual)


        # Determine fold and make new chain for every possibility.
        else:
            legal_moves = get_legal_moves_nomirror(chain_actual.chain_list[-1].get_fold_coordinates(), chain_actual)

            # if there are no legal moves chain ends here.
            if legal_moves:
                # Go trough the legal moves and make a new_chain for every move, then put them in the queue.
                for move in legal_moves:

                    atype = protein.amino_string[index]
                    coordinates = chain_actual.chain_list[-1].get_fold_coordinates()
                    # Make a new amino and add it to the a new chain with deepcopy
                    amino = Amino(atype, move, coordinates)
                    new_chain = copy.deepcopy(chain_actual)
                    new_chain.chain_list.append(amino)
                    # Put the new chain in the queue
                    queue.put(new_chain)

    # The best score and corresponding chain that has been found
    best_score = 1
    best_chains = []

    # Goes over all finished chains to find the one with the best score
    for chain in finished_chains:

        matrix, xy_offset = get_matrix_efficient(chain.chain_list)
        score = get_score_efficient(chain.chain_list, matrix, xy_offset, ch_score)

        # If the score is better than the best score, replace best_chains
        # if score is equal add chain to best_chains
        if score < best_score:
            best_score = score
            best_chains = []
            best_chains.append(chain)
        elif score == best_score:
            best_chains.append(chain)

    print("length best chains:" + str(len(best_chains)))
    # Return best chains and matrixes to the protein.
    for chain in best_chains:
        print(str(len(chain.chain_list)))
        protein1 = Protein(protein.amino_string, "2d")
        protein1.matrix, protein1.chain.chain_list = get_matrix(chain.chain_list)
        print(str(protein1.get_score()))
        for amino in protein1.chain.chain_list:
            print(amino, end="")
        print()

def beam_search(protein, ch_score, selection_levels):

    # Get chain WITH first amino already in it.
    start_chain = protein.chain

    # create queue and put the first amino in it
    queue = Queue(maxsize = 0)
    queue.put(start_chain)

    # Finished queues. Is this smart?
    finished_chains = []

    # Keeps track of scores in 1 layer
    scores = []

    # go trough the queue
    while not queue.empty():
        # get the first chain from the queue
        chain_actual = queue.get()

        # get the index from the length of the chain
        index = len(chain_actual.chain_list)
        print(index)

        saving_score = False
        selecting = False

        if index + 1 in selection_levels:
            saving_score = True
        elif index in selection_levels:
            average_score = sum(scores)/len(scores)
            selecting = True
        elif index - 1 in selection_levels:
            scores = []

        if selecting:
            chain_score = chain_actual.score
            if chain_score > average_score:
                continue

        # Last amino always has fold of 0.
        if  index + 1 == len(protein.amino_string):

            fold = 0
            atype = protein.amino_string[index]
            coordinates = chain_actual.chain_list[-1].get_fold_coordinates()
            new_amino = Amino(atype, fold, coordinates)
            chain_actual.chain_list.append(new_amino)

            # Save the chain to the finished chain list.
            finished_chains.append(chain_actual)

        # Determine fold and make new chain for every possibility
        else:
            legal_moves = get_legal_moves(chain_actual.chain_list[-1].get_fold_coordinates(), chain_actual.chain_list)

            # if there are no legal moves chain ends here
            if legal_moves:
                # go trough the legal moves and make a new_chain for every move, then put them in the queue
                for move in legal_moves:

                    atype = protein.amino_string[index]
                    coordinates = chain_actual.chain_list[-1].get_fold_coordinates()
                    # make a new amino and add it to the a new chain with deepcopy
                    amino = Amino(atype, move, coordinates)
                    new_chain = copy.deepcopy(chain_actual)
                    new_chain.chain_list.append(amino)
                    # put the new chain in the queue
                    if not saving_score:
                        queue.put(new_chain)
                    else:
                        matrix, offset = get_matrix_efficient(new_chain.chain_list)
                        score = get_score_efficient(new_chain.chain_list, matrix, offset, 1)
                        new_chain.score = score

                        queue.put(new_chain)
                        scores.append(score)

    # The best score and corresponding chain that has been found
    best_score = 1
    best_chains = []

    # Goes over all finished chains to find the one with the best score
    for chain in finished_chains:
        protein1 = Protein(protein.amino_string, "2d")
        protein1.matrix, protein1.chain = get_matrix(copy.deepcopy(chain).chain_list)

        matrix, xy_offset = get_matrix_efficient(chain.chain_list)
        score = get_score_efficient(chain.chain_list, matrix, xy_offset, ch_score)

        # If the score is better than the best score, replace best_chains
        # if score is equal add chain to best_chains
        if score < best_score:
            best_score = score
            best_chains = []
            best_chains.append(chain)
        elif score == best_score:
            best_chains.append(chain)
    print("length best chains:" + str(len(best_chains)))
    # Return best chains and matrixes to the protein.
    for chain in best_chains:
        print(str(len(chain.chain_list)))
        protein1 = Protein(protein.amino_string, "2d")
        protein1.matrix, protein1.chain.chain_list = get_matrix(chain.chain_list)
        print(str(protein1.get_score()))
        for amino in protein1.chain.chain_list:
            print(amino, end="")
        print()
        protein1.print_protein()
