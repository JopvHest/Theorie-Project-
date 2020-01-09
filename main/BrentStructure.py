import random
import os


# # Put the fold selector algo here. "from algorithms.algo_type import fold_selector"
# from algorithms.DepthSearch import fold_selector, get_legal_moves, find_best_chain
# from classes.amino import Amino, get_matrix, get_score

from algorithms.DepthSearch import fold_selector

from classes.protein import Protein


if __name__ == "__main__":

    protein1 = Protein("HPPHPPHPPHPH")
    protein1.print_map()
    print(protein1.score)
