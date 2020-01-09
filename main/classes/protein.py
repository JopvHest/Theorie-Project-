from pandas import DataFrame
from algorithms.helpers import get_matrix, get_score
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

        self.char_counter = 1

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
