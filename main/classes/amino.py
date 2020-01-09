# Represents a single amino-acid.
class Amino(object):

    def __init__(self, atype, fold, coordinates):
        self.atype = atype
        self.fold = fold
        self.coordinates = coordinates

        # Contains illegal folds for this amino based on that the next location wouldnt have legal moves.
        self.illegal_folds = []

    def __str__(self):
        directions = {"0":"@", "2":"v", "-2":"^", "1":">", "-1":"<"}
        string = str(self.atype) + " " + directions[str(self.fold)]
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

        raise Exception("fold of: " + str(self.fold) + " is invalid")
