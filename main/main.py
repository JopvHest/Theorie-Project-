import random

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search

if __name__ == "__main__":

    protein1 = Protein("HPPH")
    random_search(protein1)

    protein1.print_map()

    start_time = time.clock()
    newchain = copy.deepcopy(chain)
    amino1 = Amino("H", -2, [3,5])
    newchain.append(amino1)
    print("--- %s seconds ---" % (time.clock() - start_time))