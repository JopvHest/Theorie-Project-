import random

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search

if __name__ == "__main__":

    protein1 = Protein("HPPHPPHPPHPH")
    random_search(protein1)

    protein1.print_map()
