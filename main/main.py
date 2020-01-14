import random
import sys

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.helpers import get_fold_number

if __name__ == "__main__":

    protein1 = Protein("HHPPHHHPHHHHHPHPHPHPHPHPPPHPHPHPHPHPHP", "2d")
    depth_search_lookahead(protein1, 13)
    print(str(sys.getsizeof(protein1.chain)))
