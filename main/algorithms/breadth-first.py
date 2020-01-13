
from classes.amino import Amino




# class Graph():
#     def __init__(self):
#         self.nodes =
        




class Node(Amino):
    def __init__(self, atype, fold, coordinates, chain, index):
        # self.atype = atype
        # self.fold = fold
        # self.coordinates = coordinates

        # # Contains illegal folds for this amino based on that the next location wouldnt have legal moves.
        # self.illegal_folds = []

        self.chain = chain
        self.index = index


def breadth_search(protein):

    first_amino = Node(protein.chain[0], 2, [0,0], [], 0)
    first_amino.chain.append(first_amino)
    # put first amino in stack
    stack = [first_amino]

    

   
    # go trough stack
    for amino in stack:

        # Last amino always has fold of 0.
        if amino.index + 1 == len(protein.amino_string):
            fold = 0
            current_index = current_chain[-1].index
            index = current_index + 1
            atype = chars[index]
            amino = Node(atype, fold, coordinates, current_chain[-1], index)
            amino.chain.append(amino)

            # get score etc after this aminos are gone


        # Determine which fold to pick
        else:
            fold_selector(amino.chain, amino.index, protein.amino_string)
                


def fold_selector(current_chain, index, chars):




    # # If there is only 1 char left we've arrived at the end of a chain.
    # if index == len(chars):

    #     # Add the last char to the amino chain.
    #     current_chain.append(Amino(chars[0], 0, current_chain[-1].get_fold_coordinates()))

    # else:
        # Get legal moves on the position of that amino
        legal_moves = get_legal_moves(current_chain[-1].get_fold_coordinates(), current_chain)


        # If no legals move left, abort the chain. The protein got "stuck"
        if not legal_moves:
            return None

        # make nodes for legal moves and add them to the stack
        else:
            for move in legal_moves:
                current_index = current_chain[-1].index
                index = current_index + 1
                atype = chars[index]
                amino = Node(atype, move, coordinates, current_chain[-1], index)
                amino.chain.append(amino)

                stack.append(amino)
                return





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




        


        