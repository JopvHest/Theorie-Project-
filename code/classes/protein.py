# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.

import string

from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from classes.amino import Amino
from classes.chain import Chain
from functions.GetMatrix import get_matrix
from functions.GetScore import get_score
from functions.Visualize import get_connections


# Represents a chain of amino acids and its properties.
class Protein(object):

    def __init__(self, amino_string, mode):

        if mode in ["2d", "2D"]:
            self.mode_3d = False

        elif mode in ["3d", "3D"]:
            self.mode_3d = True

        else:
            raise Exception("Dimension mode not valid")

        # The list which contains the ordered and connected aminos.
        self.chain = Chain([])

        # The string of the protein, make it case insensitive
        self.amino_string = amino_string.upper()

        # Check if amino string contains chars other than H, C and P
        illegal_chars = list(string.ascii_uppercase)
        illegal_chars.remove("H")
        illegal_chars.remove("P")
        illegal_chars.remove("C")

        for char in self.amino_string:
            if char in illegal_chars:
                raise Exception("Amino string contains illegal chars")

        # Adds the first amino to the chain, direction is hard-coded as "up".
        if self.mode_3d == True:
            self.chain.chain_list.append(Amino(self.amino_string[0], 2, [0,0,0]))
        else:
            self.chain.chain_list.append(Amino(self.amino_string[0], 2, [0,0]))

        # Used to store the FINISHED matrix.
        self.matrix = []

        # Some functions use this to determine the char that is being "calculated"
        self.char_counter = 1

    # Prints a 2d or 3d represenation of the protein using MatPlotLib
    def print_protein(self):
        
        # Get list of bonds
        connections = get_connections(self.chain.chain_list, self.matrix)

        # 2D print
        if self.mode_3d == False:
            x_points, y_points, colors = [], [], []
            # Create lists of x/y coordinates of all amino's
            for amino in self.chain.chain_list:
                x_points.append(amino.coordinates[0])
                y_points.append(amino.coordinates[1])

                # For each amino, append colors list with appropriate color
                if amino.atype == 'H':
                    colors.append((1,0,0))
                elif amino.atype == 'P':
                    colors.append((0,0,1))
                elif amino.atype == 'C':
                    colors.append((0,1,0))

            fig, ax = plt.subplots()
            # Plot solid black line connecting amino's
            plt.plot(x_points, y_points, linestyle='-', color='black', linewidth=3, zorder=0)
            # Plot scatter points, at coordinates of amino's, in appropriate colors
            plt.scatter(x_points, y_points, c = colors, s = 200, zorder=10)

            # Plot all connections using dotted line in appropriate color, based on amount of points the connection gives
            for connection in connections:
                if connection[0] == 1:
                    plt.plot((connection[1][0], connection[2][0]), (connection[1][1], connection[2][1]), linestyle=':', color=(1,0,0))
                if connection[0] == 5:
                    plt.plot((connection[1][0], connection[2][0]), (connection[1][1], connection[2][1]), linestyle=':', color=(0,1,0))

            # Set grid size to 1x1
            ax.xaxis.set_major_locator(plt.MultipleLocator(1))
            ax.yaxis.set_major_locator(plt.MultipleLocator(1))

            # Scale all axis equally, show grid, and show plot
            plt.axis("equal")
            plt.grid()
            plt.show()

        # 3D print
        if self.mode_3d == True:
            x_points, y_points, z_points, colors = [], [], [], []
            # Create lists of x/y/z coordinates of all amino's
            for amino in self.chain.chain_list:
                x_points.append(amino.coordinates[0])
                y_points.append(amino.coordinates[1])
                z_points.append(amino.coordinates[2])

                # Append colors list with appropriate color per amino
                if amino.atype == 'H':
                    colors.append((1,0,0))
                elif amino.atype == 'P':
                    colors.append((0,0,1))
                elif amino.atype == 'C':
                    colors.append((0,1,0))

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Create scatter plot with all amino's
            ax.scatter(x_points, y_points, z_points, c = colors, s = 200)
            # Plot line connecting amino's
            ax.plot(x_points, y_points, z_points, linestyle='-', color='black')

            # Plot each bond in appropriate color
            for connection in connections:
                if connection[0] == 1:
                    plt.plot((connection[1][0], connection[2][0]), (connection[1][1], connection[2][1]), (connection[1][2], connection[2][2]), linestyle=':', color=(1,0,0))
                if connection[0] == 5:
                    plt.plot((connection[1][0], connection[2][0]), (connection[1][1], connection[2][1]), (connection[1][2], connection[2][2]), linestyle=':', color=(0,1,0))

            # Following code is a workaround to scale the axis equally in 3d
            max_range = max(max(x_points) - min(x_points), max(y_points) - min(y_points), max(z_points) - min(z_points)) / 2
            mid_x = (max(x_points) + min(x_points)) * 0.5
            mid_y = (max(y_points) + min(y_points)) * 0.5
            mid_z = (max(z_points) + min(z_points)) * 0.5

            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)

            ax.xaxis.set_major_locator(plt.MultipleLocator(1))
            ax.yaxis.set_major_locator(plt.MultipleLocator(1))
            ax.zaxis.set_major_locator(plt.MultipleLocator(1))

            # Label axis
            ax.set_xlabel('X Axis')
            ax.set_ylabel('Y Axis')
            ax.set_zlabel('Z Axis')

            # Create grid and show plot
            ax.grid()
            plt.show()


    # Outputs a list like the excercise requires
    def get_output_list(self):

        print("amino, fold, coordinates")
        for amino in self.chain.chain_list:
            print(str(amino.get_amino_output()))
        print("")

    # Returns the score
    def get_score(self):
        return get_score(self.chain.chain_list, self.matrix)
