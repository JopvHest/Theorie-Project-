
from classes.amino import Amino



class Node(object):
    def __init__(self, atype, fold, coordinates, index):
        self.atype = atype
        self.fold = fold
        self.coordinates = coordinates

        # # Contains illegal folds for this amino based on that the next location wouldnt have legal moves.
        # self.illegal_folds = []

        self.chain = []
        self.index = index

    def __str__(self):
        return self.atype + str(self.chain)

    
    # Get the amino output for the standard output we need.
    def get_amino_output(self):
        return str((self.atype, self.fold, self.coordinates))

    # Gets the x,y of the next amino in the chain.
    def get_fold_coordinates(self):

        # Amino has no fold because its the last in the chain.
        if self.fold == 0:
            return False


        fold_coordinates = list(self.coordinates)

        # Fold is in y direction.
        if abs(self.fold) == 2:
            # We want the coordinates to stay a int.
            fold_coordinates[1] += int(self.fold / 2)
            return fold_coordinates

        # Fold is in x direction.
        if abs(self.fold) == 1:
            fold_coordinates[0] += self.fold
            return fold_coordinates
        
        # Fold is in Z direction.
        if abs(self.fold) == 3:
            fold_coordinates[2] += int(self.fold / 3)
            return fold_coordinates

        raise Exception("fold of: " + str(self.fold) + " is invalid")


def breadth_search(protein):

    first_amino = Node(protein.chain[0], 2, [0,0], 0)
    first_amino.chain.append(first_amino)
    # put first amino in stack
    stack = [first_amino]

    

   
    # go trough stack
    for amino in stack:

        # Last amino always has fold of 0.
        # + 2 because index starts at 0 and you want to add last node one before the end
        if amino.index + 2 == len(protein.amino_string):
            
            fold = 0
            index = amino.chain[-1].index + 1
            
            amino_chain = amino.chain[-1]
            atype = protein.amino_string[index]
            coordinates = amino.chain[-1].get_fold_coordinates()
            amino = Node(atype, fold, coordinates, index)
            amino.chain = amino_chain.chain
            amino.chain.append(amino)

            # get score etc after this aminos are gone


        # Determine which fold to pick
        else:
            new_amino = fold_selector(amino.chain, amino.index, protein.amino_string)
            stack.append(new_amino)
                


def fold_selector(current_chain, index, chars):




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
            coordinates = current_chain[-1].get_fold_coordinates()
            amino = Node(atype, move, coordinates, index)
            amino.chain = current_chain[-1].chain
            amino.chain.append(amino)
            # stack.append(amino)
            return amino





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




        


        