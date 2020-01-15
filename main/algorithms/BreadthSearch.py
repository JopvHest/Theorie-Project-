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
from queue import Queue
import copy
from classes.protein import Protein

from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient
from functions.GetLegalMoves import get_legal_moves


def breadth_search(protein, ch_score):

    # Get chain WITH first amino already in it.
    start_chain = protein.chain

    # create queue and put the first amino in it
    queue = Queue(maxsize = 0)
    queue.put(start_chain)

    # Finished queues. Is this smart?
    finished_chains = []

    # go trough the queue
    while not queue.empty():
        # get the first chain from the queue
        chain_actual = queue.get()

        # get the index from the length of the chain
        index = len(chain_actual)

        # Last amino always has fold of 0.
        if  index + 1 == len(protein.amino_string):

            fold = 0
            atype = protein.amino_string[index]
            coordinates = chain_actual[-1].get_fold_coordinates()
            new_amino = Amino(atype, fold, coordinates)
            chain_actual.append(new_amino)

            # Save the chain to the finished chain list.
            finished_chains.append(chain_actual)

        # Determine fold and make new chain for every possibility
        else:
            legal_moves = get_legal_moves(chain_actual[-1].get_fold_coordinates(), chain_actual)

            # if there are no legal moves chain ends here
            if legal_moves:
                # go trough the legal moves and make a new_chain for every move, then put them in the queue
                for move in legal_moves:

                    atype = protein.amino_string[index]
                    coordinates = chain_actual[-1].get_fold_coordinates()
                    # make a new amino and add it to the a new chain with deepcopy
                    amino = Amino(atype, move, coordinates)
                    new_chain = copy.deepcopy(chain_actual)
                    new_chain.append(amino)
                    # put the new chain in the queue
                    queue.put(new_chain)

    # The best score and corresponding chain that has been found
    best_score = 1
    best_chains = []

    # Goes over all finished chains to find the one with the best score
    for chain in finished_chains:

        matrix, xy_offset = get_matrix_efficient(chain)
        score = get_score_efficient(chain, matrix, xy_offset,  ch_score)

        # If the score is better than the best score, replace best_chains
        # if score is equal add chain to best_chains
        if score < best_score:
            best_score = score
            best_chains = []
            best_chains.append(chain)
        if score == best_score:
            best_chains.append(chain)

    # Return best chains and matrixes to the protein.
    for chain in best_chains:
        print(str(len(chain)))
        protein1 = Protein(protein.amino_string, "2d")
        protein1.matrix, protein1.chain = get_matrix(chain)
        print(str(protein1.get_score()))
        for amino in protein1.chain:
            print(amino, end="")
        protein1.print_protein()
