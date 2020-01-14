import random

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.helpers import get_fold_number
from algorithms.breadth_first import breadth_search


if __name__ == "__main__":

<<<<<<< HEAD
    protein1 = Protein("HPPHPCPPHPPHPHCH", "2D")
    breadth_search(protein1)
=======
    protein1 = Protein("HHPPPPPPHH", "2D")
    depth_search(protein1)

    protein1.print_map()
    protein1.print_protein()
>>>>>>> 2d223c0d7a3a3aebbfef46a1d1686f1d043f70ea
