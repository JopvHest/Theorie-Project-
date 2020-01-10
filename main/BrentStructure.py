import random
import time

from classes.protein import Protein
from algorithms.helpers import get_matrix
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search

if __name__ == "__main__":

    start_time = time.clock()
    protein1 = Protein("HPPHPHPHPPHHPH")
    depth_search(protein1)
    protein1.print_map()
    protein1.get_output_list()


    print("--- %s seconds ---" % (time.clock() - start_time))