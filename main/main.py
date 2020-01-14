import random
import sys

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.helpers import get_fold_number
from algorithms.BreadthSearch import breadth_search


if __name__ == "__main__":

    protein1 = Protein("HHcPPphhpphppphphhhhppphphphpphhhhhhhhPPPcPhphcPH", "3D")
    depth_search_lookahead(protein1, 5)
    protein1.print_protein()
