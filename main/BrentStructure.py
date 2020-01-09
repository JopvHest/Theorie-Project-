import random
import os

from classes.protein import Protein
from algorithms.helpers import get_matrix
from algorithms.RandomSearch import random_chain
from algorithms.DepthSearch import depth_chain

if __name__ == "__main__":

    protein1 = Protein("HPPHPPHPPHPH")
    random_chain(protein1)
    protein1.print_map()
