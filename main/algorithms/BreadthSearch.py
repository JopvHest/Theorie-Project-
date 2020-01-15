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

from functions.GetMatrix import get_matrix_efficient, get_matrix
from functions.GetScore import get_score_efficient


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
    best_chain = []

    # Goes over all finished chains to find the one with the best score
    for chain in finished_chains:

        matrix, xy_offset = get_matrix_efficient(chain)
        score = get_score_efficient(chain, matrix, xy_offset, ch_score)

        # If the score is better than the best score, replace best_chain
        if score < best_score:
            best_score = score
            best_chain = chain

    # Return best chain and matrix to the protein.
    protein.matrix, protein.chain = get_matrix(best_chain)

    print("Score: ", end="")
    print(protein.get_score(ch_score))
    for amino in protein.chain:
        print(str(amino), end="")



def get_legal_moves(xy, chain):

    # This is a list of tuples with 1: the move, 2: the coordinates delta that cant exist yet.
    moves_xydelta = [[1, (1, 0)], [-1, (-1, 0)], [2, (0, 1)], [-2, (0, -1)]]

    # Check if the legal moves interfere with any of the current amino coordinates.
    # Note: we iterate over a COPY of the list because you cant delete items from a list while iterating over it.
    for amino in list(chain):
        # Check for every legal move left.
        for move in moves_xydelta:

            # If the move delta plus current xy is equal to another amino's xy remove it from the legal moves list.
            coordinates_sum = []
            coordinates_sum.append(move[1][0] + xy[0])
            coordinates_sum.append(move[1][1] + xy[1])

            if coordinates_sum == list(amino.coordinates):
                moves_xydelta.remove(move)

    # Only return the move int of the legal moves remaining.
    legal_moves = []
    for moves in moves_xydelta:
        legal_moves.append(moves[0])

    return legal_moves
