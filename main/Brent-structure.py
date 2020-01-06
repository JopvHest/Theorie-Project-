# Represents a single amino-acid.
class Amino(object):
    
    def __init__(self, atype, fold, coordinates):
        self.atype = atype
        self.fold = fold
        self.coordinates = coordinates
    
    # Gets the x,y of the next amino in the chain.
    def get_fold_coordinates(self):
        
        # Amino has no fold because its the last in the chain.
        if self.fold == 0:
            return False


        fold_coordinates = list(self.coordinates)

        # Fold is in y direction.
        if abs(self.fold) == 2:
            fold_coordinates[1] += self.fold / 2
            return tuple(fold_coordinates)
        
        # Fold is in x direction.
        if abs(self.fold) == 1:
            fold_coordinates[0] += self.fold
            return tuple(fold_coordinates)
        
        raise Exception("fold of: " + str(self.fold) + " is invalid")

# Represents a chain of amino acids and orders them.
class Protein(object):

    def __init__(self, amino_string, algo):
        
        # The list which contains the ordered and conneceted aminos.
        self.chain = []

        # Adds the first amino to the chain, direction is hard-coded as "up"
        self.chain.append(Amino(amino_string[0], 2, (0,0)))

        for char in amino_string:
            fold = algo_selector(amino, algo)



if __name__ == "__main__":
  