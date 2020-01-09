# Represents a single amino-acid.
class Amino(object):

    def __init__(self, atype, fold, coordinates):
        self.atype = atype
        self.fold = fold
        self.coordinates = coordinates

        # Contains illegal folds for this amino based on that the next location wouldnt have legal moves.
        self.illegal_folds = []

    def __str__(self):
        directions = {"0":"@", "2":"^", "-2":"v", "1":">", "-1":"<"}
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


# Takes the chain and makes a 2d matrix out of it. Returns a matrix and a ofsetted chain
def get_matrix(chain):

    x_range = [0, 0]
    y_range = [0, 0]

    # Define min/max x and y values over all aminos.
    for amino in chain:
        if amino.coordinates[0] > x_range[1]:
            x_range[1] = amino.coordinates[0]
        elif amino.coordinates[0] < x_range[0]:
            x_range[0] = amino.coordinates[0]
        if amino.coordinates[1] > y_range[1]:
            y_range[1] = amino.coordinates[1]
        elif amino.coordinates[1] < y_range[0]:
            y_range[0] = amino.coordinates[1]

    # Adjust amino coordinates so no negative values remain.
    for amino in chain:
        amino.coordinates[0] -= x_range[0]
        amino.coordinates[1] -= y_range[0]

    matrix = []

    # Fill matrix with placeholder values.
    for i in range(y_range[1] - y_range[0] + 1):
        row = []
        for j in range(x_range[1] - x_range[0] + 1):
            row.append(" ")
        matrix.append(row)

    
    # Adds aminos to matrix.
    for amino in chain:
        matrix[amino.coordinates[1]][amino.coordinates[0]] = amino

    return matrix, chain


# This function calculates and returns the score of the chain
def get_score(chain, matrix):
    
        total_score = 0
        
        # Iterate over all aminos and add the score of all of them.
        for index, amino in enumerate(chain):
            
            # P has no effect on stability
            if amino.atype == "P":
                continue
            
            # Creates a list with all coordinates that need to be checked.
            xy_tocheck = []
            amino_x, amino_y = amino.coordinates
            xy_tocheck.append([amino_x + 1, amino_y])
            xy_tocheck.append([amino_x, amino_y + 1])
            xy_tocheck.append([amino_x - 1, amino_y])
            xy_tocheck.append([amino_x, amino_y - 1])

            # Aminos to and from that amino dont add to the score so remove them.
            if amino.get_fold_coordinates() in xy_tocheck:
                xy_tocheck.remove(amino.get_fold_coordinates())
            
            if chain[index - 1].coordinates in xy_tocheck:
                xy_tocheck.remove(chain[index - 1].coordinates)

            # Check all coordinates around it and adjust score if a H is next to it.
            for x, y in xy_tocheck:
                if y < len(matrix) and y >= 0:
                    if  x < len(matrix[0]) and x >= 0:
                        if isinstance(matrix[y][x], Amino):
                            if matrix[y][x].atype == "H":
                                total_score -= 1
        total_score = total_score // 2
        return total_score 