import random
from pandas import DataFrame

import os


# Put the fold selector algo here. "from algorithms.algo_type import fold_selecto"r"
from algorithms.BreadthSearch import fold_selector, get_legal_moves, find_best_chain
# from algorithms.RandomAlgo import fold_selector, get_legal_moves
from algorithms.Amino import Amino, get_matrix, get_score

# Represents a chain of amino acids and orders them.
class Protein(object):

    def __init__(self, amino_string):

        # The list which contains the ordered and conneceted aminos.
        self.chain = []

        # Adds the first amino to the chain, direction is hard-coded as "up".
        self.chain.append(Amino(amino_string[0], 2, [0,0]))

        # IF a ideal answer is found, it is stored here
        self.ideal_chain = []

        self.char_counter = 1
        # Skips the first char the index.
        while self.char_counter < len(amino_string):
            
            # Ideal chain is already found, replace chain with ideal chain and break loop.
            if self.ideal_chain:
                self.chain = self.ideal_chain
                break
            
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
                fold, self.ideal_chain = fold_selector(amino_xy, char, self.chain, illegal_folds, amino_string)

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

if __name__ == "__main__":
    
    protein1 = Protein("HPPHPPHPPHPH")
    protein1.print_map()
    print(protein1.score)
