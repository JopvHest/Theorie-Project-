import random


# Represents a single amino-acid.
class Amino(object):
    
    def __init__(self, atype, fold, coordinates):
        self.atype = atype
        self.fold = fold
        self.coordinates = coordinates
        
        # Contains illegal folds for this amino based on that the next location wouldnt have legal moves.
        self.illegal_folds = []
    
    def __str__(self):
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
        
        raise Exception("fold of: " + str(self.fold) + " is invalid")
    

# Represents a chain of amino acids and orders them.
class Protein(object):

    def __init__(self, amino_string):
        
        # The list which contains the ordered and conneceted aminos.
        self.chain = []

        # Adds the first amino to the chain, direction is hard-coded as "up".
        self.chain.append(Amino(amino_string[0], 2, [0,0]))
    	
        self.char_counter = 1
        # Skips the first char the index.
        while self.char_counter < len(amino_string):
            print(str(self.char_counter))
            char = amino_string[self.char_counter]
            # Get the location the last amino folded to.
            # Note: an index of -1 gets the last object in a list.
            amino_xy = self.chain[-1].get_fold_coordinates()

            
            # Last amino always has fold of 0.
            if self.char_counter + 1 == len(amino_string):
                fold = 0
            
            # Determine which fold to pick
            else:
                illegal_folds = None
                fold = fold_selector(amino_xy, char, self.chain, illegal_folds)

                 # If no legal moves are available, the last move needs to be reversed.
                if not fold:
                    self.redo_last_fold()
                    continue
            
            # Adds amino to the protein chain. 
            self.chain.append(Amino(char, fold, amino_xy))
            self.char_counter += 1
           
        

    # Outputs a list like the excercise requires
    def get_output_list(self):

        print("amino, fold")
        for amino in self.chain:
            print(amino.atype + ", " + str(amino.fold) + str(amino.coordinates))
        print("")

    # Prints a very shitty 2d map of the protein.
    def print_map(self):
        
        # Here we shift the coordinates to start from 0 and not go under that.
        x_range = [0, 0]
        y_range = [0, 0]

        chain_shifted = self.chain
        
        # Find lowest and highest values for x and y
        for amino in chain_shifted:
            
            if amino.coordinates[0] > x_range[1]:
                x_range[1] = amino.coordinates[0]
            if amino.coordinates[0] < x_range[0]:
                x_range[0] = amino.coordinates[0]
            
            if amino.coordinates[1] > y_range[1]:
                y_range[1] = amino.coordinates[1]
            if amino.coordinates[1] < y_range[0]:
                y_range[0] = amino.coordinates[1]
        print("x-range =" + str(x_range) + ", y-range =" + str(y_range))
        print("")

        # Adjust the amino coordinates to start at 0
        for amino in chain_shifted:
            amino.coordinates[0] -= x_range[0]
            amino.coordinates[1] -= y_range[0]
        
        print("adjusted x/y: ")
        for amino in chain_shifted:
            print(str(amino.coordinates))
        print("")
        
        # Print the x coordinates
        for x in range(x_range[1] - x_range[0] + 1):
            print( "       " + str(x) + "       ", end="")
        print("")

        for row in range(0, y_range[1] - y_range[0] + 1):
            
            # Print the y coordinates
            print( str(row), end="")
            
            for column in range(x_range[1] - x_range[0] + 1):
                
                #Iterate through all the aminos to see if one has these coordinates
                print_x = True
                for amino in chain_shifted:
                    if amino.coordinates == [column, row]:
                        print(amino, end="")
                        print_x = False
                        break
                if print_x:
                    print("       x       ", end="")
 
            print("")

    def get_score(self):
        #TODO
        pass

    def redo_last_fold(self):
        print("redo")
        # Store the illegal fold in the amino class.
        last_amino = self.chain[-1]
        last_amino.illegal_folds.append(last_amino.fold)

        print(last_amino.fold)

        # Get new move with illegal moves excluded.
        fold = fold_selector(last_amino.coordinates, last_amino.atype, self.chain[:-1], last_amino.illegal_folds)
        
        # Replace the previous illegal fold with a new fold
        last_amino.fold = fold
        print(fold)
        print("test34")


        # If still no fold found, also redo move before that. Char loop in init needs to go back 1 step.
        if not fold:
            self.chain.remove(last_amino)
            self.char_counter -= 1
            self.redo_last_fold()
                


# The actual algo for selecting the fold the chain will make.
def fold_selector(xy, char, chain, illegal_moves):
    
    legal_moves = get_legal_moves(xy, chain)
    
    # Remove illegal moves from legal moves list.
    if illegal_moves:  
        for move in illegal_moves:
            if move in legal_moves:
                legal_moves.remove(move)
            
    # Selects a random move if at least 1 legal moves exists
    if legal_moves:
        return random.choice(legal_moves)

    # If no legal moves exist, return False
    return False
    

    # Finds all the legal moves that can be made from the current position.
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

if __name__ == "__main__":
    protein1 = Protein("HPHPHPHHHPPHPPHPHPHPHHPPHP")
    protein1.get_output_list()
    protein1.print_map()