import random
import time

from classes.protein import Protein
from algorithms.helpers import get_matrix, get_score
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead

# Wanted to try if implementing multithreading was an easy performance boost. Seems pretty hard to implement.
# Might try again later.
from multiprocessing.dummy import Pool as ThreadPool 



if __name__ == "__main__":

    start_time = time.clock()
    
    protein1 = Protein("HPPHPPHHPHHPPHPPHHPHHPPHPPHHPHHPPHPPHHPHHPPHPPHHPH", "3d")
    
    depth_search_lookahead(protein1, 5)
    protein1.print_map()
    protein1.get_output_list()
    print(str(get_score(protein1.chain, protein1.matrix)))

    print("--- %s seconds ---" % (time.clock() - start_time))
    