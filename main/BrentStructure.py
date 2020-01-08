import random
from pandas import DataFrame

import os


# Put the fold selector algo here. "from algorithms.algo_type import fold_selecto"r"
from algorithms.RandomAlgo import fold_selector, get_legal_moves

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
            # print(str(self.char_counter))
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

        # for amino in self.chain:
            # print(str(amino))
        # Save a matrix version of the chain.
        # We also update the chain to a ofsetted version of the chain.(it now starts from x, y = 0, 0)
        self.matrix, self.chain = get_matrix(self.chain)

        # for amino in self.chain:
            # print(amino.get_amino_output())

        # Get the score of the protein and print it.
        self.score = get_score(self.chain, self.matrix)

    # Prints the matrix of the protein.
    def print_map(self):
        matrix = self.matrix


        # Print matrix using pandas
        print(DataFrame(matrix))

    # Outputs a list like the excercise requires
    def get_output_list(self):

        print("amino, fold")
        for amino in self.chain:
            print(str(amino.get_amino_output()))
        print("")

    def redo_last_fold(self):
        # Store the illegal fold in the amino class.
        last_amino = self.chain[-1]
        last_amino.illegal_folds.append(last_amino.fold)

        # Get new move with illegal moves excluded.
        fold = fold_selector(last_amino.coordinates, last_amino.atype, self.chain[:-1], last_amino.illegal_folds)

        # Replace the previous illegal fold with a new fold
        last_amino.fold = fold


        # If still no fold found, also redo move before that. Char loop in init needs to go back 1 step.
        if not fold:
            self.chain.remove(last_amino)
            self.char_counter -= 1
            self.redo_last_fold()


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


if __name__ == "__main__":
    protein1 = Protein("HHPHPPHPHPHPHPHPHHH")

    lowest_score = 0
    for i in range(10):
        for i in range(5000):
            protein1 = Protein("PHPPHPPHPPH")
            if protein1.score < lowest_score:
                lowest_score = protein1.score
                best_protein = protein1
        print( str(i) + " runs, lowest score:" + str(lowest_score))

    best_protein.print_map()
