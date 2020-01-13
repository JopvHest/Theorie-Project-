from pandas import DataFrame
from algorithms.helpers import get_matrix, get_score
from classes.amino import Amino

import string

import matplotlib.pyplot as plt


# Represents a chain of amino acids and orders them.
class Protein(object):

    def __init__(self, amino_string, mode):

        if mode == "2d" or mode == "2D":
            self.mode_3d = False

        elif mode == "3d" or mode == "3D":
            self.mode_3d = True

        else:
            raise Exception("Dimension mode not valid")

        # The list which contains the ordered and connected aminos.
        self.chain = []


        # The string of the protein, make it case insensitive
        self.amino_string = amino_string.upper()

        # Check if amino string contains chars other than H, C and P
        illegal_chars = list(string.ascii_uppercase)
        illegal_chars.remove("H")
        illegal_chars.remove("P")
        illegal_chars.remove("C")

        for char in amino_string:
            if char in illegal_chars:
                raise Exception("Amino string contains illegal chars")

        # Adds the first amino to the chain, direction is hard-coded as "up".
        if self.mode_3d == True:
            self.chain.append(Amino(amino_string[0], 2, [0,0,0]))
        else:
            self.chain.append(Amino(amino_string[0], 2, [0,0]))

        # IF a ideal answer is found, it is stored here
        self.ideal_chain = []

        self.matrix = []

        self.char_counter = 1

    # Prints the matrix of the protein.
    def print_map(self):

        if self.mode_3d == False:
            matrix = self.matrix
            # Print matrix using pandas
            print(DataFrame(matrix))

        if self.mode_3d == True:
            matrix = self.matrix

            # go through each layer and print it
            for layer in matrix:
                # Print matrix using pandas
                print(DataFrame(layer))

    def print_protein(self):
        if self.mode_3d == False:
            x_points, y_points, colors = [], [], []
            for amino in self.chain:
                x_points.append(amino.coordinates[0])
                y_points.append(amino.coordinates[1])

                if amino.atype == 'H':
                    colors.append((1,0,0))
                elif amino.atype == 'P':
                    colors.append((0,0,1))

            fig, ax = plt.subplots()
            plt.scatter(x_points, y_points, c = colors, s = 200)
            plt.plot(x_points, y_points, linestyle='-', color='0.4')
            ax.xaxis.set_major_locator(plt.MultipleLocator(1))
            ax.yaxis.set_major_locator(plt.MultipleLocator(1))
            plt.grid()

            plt.show()

        if self.mode_3d == True:
            print("3D version not yet implemented. ")

    # Outputs a list like the excercise requires
    def get_output_list(self):

        print("amino, fold")
        for amino in self.chain:
            print(str(amino.get_amino_output()))
        print("")

    def get_score(self):
        return get_score(self.chain)
