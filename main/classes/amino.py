# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.

# Represents a single amino-acid.
class Amino(object):

    def __init__(self, atype, fold, coordinates):
        # The type of the amino, so: "C",  "H" or "P"
        self.atype = atype
        
        # Check if fold is legal and save it.
        legal_folds = [1, -1, 2, -2, 3, -3, 0]
        if fold not in legal_folds:
            raise Exception("Invalid fold.")
        self.fold = fold

        # The 2d OR 3d coordinates in a list [x, y] or [x, y, z]
        self.coordinates = coordinates

        # Contains illegal folds for this amino based on that the next location wouldnt have legal moves.
        # Only used in Random.
        self.illegal_folds = []

        # Contains the chain of Aminos in a list.
        self.chain = []


    # Returns the type plus the direction of the fold.
    def __str__(self):
        directions = {"0":"@", "2":"v", "-2":"^", "1":">", "-1":"<", "3": "O", "-3" : "X"}
        string = str(self.atype) + directions[str(self.fold)] + " "
        return string

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
