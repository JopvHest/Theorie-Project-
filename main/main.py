import sys, time

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.BreadthSearch import breadth_search


if __name__ == "__main__":

    protein1 = Protein("Hphhchhhp", "3D")
    depth_search(protein1, 1)
    print(protein1.get_score())
    protein1.print_protein()
