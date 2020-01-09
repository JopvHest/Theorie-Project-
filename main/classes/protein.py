from pandas import DataFrame

from classes.amino import Amino

# Represents a chain of amino acids and orders them.
class Protein(object):

    def __init__(self, amino_string):

        # The list which contains the ordered and connected aminos.
        self.chain = []

        self.amino_string = amino_string

        # Adds the first amino to the chain, direction is hard-coded as "up".
        self.chain.append(Amino(amino_string[0], 2, [0,0]))

        # IF a ideal answer is found, it is stored here
        self.ideal_chain = []

        self.matrix = []

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
