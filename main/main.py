import sys, time

from classes.protein import Protein
from classes.amino import Amino
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.BreadthSearch import breadth_search

from functions.GetMatrix import get_matrix_efficient
from functions.GetScore import get_score_efficient


if __name__ == "__main__":

    # chain = [Amino("H", 2, [0,0]), Amino("H", 2, [0,1]), Amino("H", 1, [0,2]), Amino("P", -2, [1,2]), Amino('H', -2, [1,1]), Amino("H", 1, [1, 0]), Amino("P", 2, [2, 0]), Amino("H", 0, [2,1])]
    start_time = time.clock()
    
    protein1 = Protein("HHPPpphph", "3D")

    depth_search(protein1, 1)
    protein1.print_protein()
    print("--- %s seconds ---" % (time.clock() - start_time))
    

    # matrix, offset = get_matrix_efficient(chain)


    
   
    

    
    # protein1 = Protein("HPPHHHPPHHPH", "2D")
    # depth_search(protein1, 0.5)
    

    # start_time = time.clock()
    


