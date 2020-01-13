import random

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.helpers import get_fold_number

if __name__ == "__main__":




    protein1 = Protein("HPPHhhPPPHHHH")
    random_search(protein1)
    folds = get_fold_number(protein1.chain)
    print(folds)

    # protein1.print_map()

    # start_time = time.clock()
    # newchain = copy.deepcopy(chain)
    # amino1 = Amino("H", -2, [3,5])
    # newchain.append(amino1)
    # print("--- %s seconds ---" % (time.clock() - start_time))