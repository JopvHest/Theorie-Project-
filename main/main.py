import random
import sys

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.helpers import get_fold_number
from algorithms.BreadthSearch import breadth_search


if __name__ == "__main__":

    protein1 = Protein("HHPPPPP", "2D")
    breadth_search(protein1)

    # protein1 = Protein("HPPCPPCHHHHPHHPPP", "2D")
    # depth_search_lookahead(protein1, 10)

    # protein1.print_map()
    # protein1.print_protein()
